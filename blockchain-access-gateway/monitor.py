#!/usr/bin/env python3
"""
monitor.py  -  runs on the KALI (defender) machine.
Reads Suricata's alert log; on each attack it records the attacker's IP on the
blockchain, and sends a Telegram alert. Blocks whatever IP Suricata flags
(no hardcoded attacker IP), ignoring only this machine and local noise.
"""
import json, time, requests
from contract_address import CONTRACT_ADDRESS
from web3 import Web3

# ========== CONFIG - EDIT THESE ==========
KALI_IP            = "172.16.197.21"     # THIS (defender) machine - never block ourselves
RPC_URL            = "http://127.0.0.1:8545"
PRIVATE_KEY        = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # Hardhat test key #0
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"    # get from @BotFather
TELEGRAM_CHAT_ID   = "YOUR_CHAT_ID"      # get from @userinfobot
# =========================================

ABI = '[{"inputs":[{"internalType":"string","name":"ip","type":"string"}],"name":"blockIP","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"ip","type":"string"}],"name":"isBlocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBlockedIPs","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"}]'

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=5)
    except Exception as e:
        print(f"Telegram error: {e}")

def block_ip(ip, signature):
    print(f"Blocking attacker {ip} ...")
    send_telegram(f"<b>ATTACK DETECTED!</b>\nIP: <code>{ip}</code>\nSignature: {signature}\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        account = w3.eth.account.from_key(PRIVATE_KEY)
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        tx = contract.functions.blockIP(ip).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': w3.eth.gas_price
        })
        signed = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f"{ip} recorded on-chain")
            send_telegram(f"<b>{ip} blocked on blockchain!</b>\nTX: {tx_hash.hex()}")
        else:
            send_telegram(f"<b>Failed to block {ip}</b>")
    except Exception as e:
        print(f"Error: {e}")
        send_telegram(f"<b>Error:</b> {str(e)}")

def follow_log():
    with open('/var/log/suricata/eve.json') as f:
        f.seek(0, 2)               # jump to end - only read NEW lines
        while True:
            line = f.readline()
            if line:
                yield line.strip()
            else:
                time.sleep(0.5)

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not w3.is_connected():
    print("Cannot connect to Hardhat node! Start it first: npx hardhat node")
    exit(1)

print("KALI DEFENDER STARTED - watching for attacks ...")
seen = set()
for line in follow_log():
    try:
        alert = json.loads(line)
        if alert.get('event_type') == 'alert' and 'src_ip' in alert:
            src_ip = alert['src_ip']
            sig = alert['alert'].get('signature', 'Unknown')
            if src_ip == KALI_IP or src_ip.startswith(("127.", "169.254.")):
                continue
            if src_ip in seen:           # block each attacker only once
                continue
            seen.add(src_ip)
            print(f"ATTACK FROM {src_ip}: {sig}")
            block_ip(src_ip, sig)
    except Exception:
        pass
