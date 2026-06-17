#!/usr/bin/env python3
"""
monitor.py - KALI (defender). Reads Suricata alerts; records the attacker IP on
the blockchain and prints a FULL alert to THIS terminal. Also tries Telegram,
but the terminal alert always works even when Telegram is unreachable.
"""
import json, time, requests
from contract_address import CONTRACT_ADDRESS
from web3 import Web3

# ========== CONFIG ==========
KALI_IP            = "172.16.32.119"
RPC_URL            = "http://127.0.0.1:8545"
PRIVATE_KEY        = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID   = "YOUR_CHAT_ID"
ONLY_NMAP_SCANS    = True   # True = block only nmap scans (clean demo). False = block any alert.
# ============================

ABI = '[{"inputs":[{"internalType":"string","name":"ip","type":"string"}],"name":"blockIP","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"ip","type":"string"}],"name":"isBlocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBlockedIPs","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"}]'

def banner(lines):
    w = 64
    print("\n" + "=" * w)
    for ln in lines:
        print(ln)
    print("=" * w + "\n")

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=5)
    except Exception:
        print("[i] Telegram unreachable - full alert is shown above in this terminal.")

def block_ip(d):
    ip, sig = d['src_ip'], d['signature']
    ts = time.strftime('%Y-%m-%d %H:%M:%S')

    # ---- FULL ALERT printed to this terminal (always works) ----
    banner([
        "   *** ATTACK DETECTED ***",
        f"   Attacker IP : {ip}",
        f"   Attack type : {sig}",
        f"   Category    : {d['category']}",
        f"   Severity    : {d['severity']}",
        f"   Target      : {d['dest_ip']}:{d['dest_port']}  ({d['proto']})",
        f"   Detected at : {ts}",
        "   Action      : recording on the blockchain ...",
    ])

    send_telegram(f"<b>ATTACK DETECTED!</b>\nIP: <code>{ip}</code>\nType: {sig}\nCategory: {d['category']}\nTime: {ts}")

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
            txid = tx_hash.hex()
            banner([
                "   *** BLOCKED ON BLOCKCHAIN ***",
                f"   Attacker IP : {ip}",
                f"   TX hash     : {txid}",
                f"   {ip} is now permanently on the on-chain blocklist.",
            ])
            send_telegram(f"<b>{ip} blocked on blockchain!</b>\nTX: {txid}")
        else:
            print(f"[!] Transaction reverted for {ip}")
    except Exception as e:
        print(f"[!] Blockchain error: {e}")

def follow_log():
    with open('/var/log/suricata/eve.json') as f:
        f.seek(0, 2)
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

print("KALI DEFENDER STARTED - watching for attacks ...\n")
seen = set()
for line in follow_log():
    try:
        alert = json.loads(line)
        if alert.get('event_type') == 'alert' and 'src_ip' in alert:
            src_ip = alert['src_ip']
            a = alert.get('alert', {})
            sig = a.get('signature', 'Unknown')
            if src_ip == KALI_IP or src_ip.startswith(("127.", "169.254.")):
                continue
            if ONLY_NMAP_SCANS and "NMAP" not in sig.upper():
                continue
            if src_ip in seen:
                continue
            seen.add(src_ip)
            block_ip({
                'src_ip': src_ip,
                'signature': sig,
                'category': a.get('category', 'N/A'),
                'severity': a.get('severity', 'N/A'),
                'dest_ip': alert.get('dest_ip', 'N/A'),
                'dest_port': alert.get('dest_port', 'N/A'),
                'proto': alert.get('proto', 'N/A'),
            })
    except Exception:
        pass
	
