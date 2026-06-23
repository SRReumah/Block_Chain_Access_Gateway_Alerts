#!/usr/bin/env python3
"""
gateway.py  -  runs on the KALI (defender) machine.
A web service (the "gateway"). Every visitor's IP is checked against the
on-chain blocklist; blocked IPs are denied access.
"""
from flask import Flask, request, jsonify
from web3 import Web3
from contract_address import CONTRACT_ADDRESS

RPC_URL = "http://127.0.0.1:8545"
app = Flask(__name__)

ABI = '[{"inputs":[{"internalType":"string","name":"ip","type":"string"}],"name":"isBlocked","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBlockedIPs","outputs":[{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"}]'

w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

@app.route('/')
def index():
    client_ip = request.remote_addr
    try:
        if contract.functions.isBlocked(client_ip).call():
            return f"ACCESS DENIED - Your IP {client_ip} is blocked!"
        return f"ACCESS ALLOWED - Your IP {client_ip} is clean."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/blocked')
def blocked():
    return jsonify({"blocked_ips": contract.functions.getBlockedIPs().call()})

if __name__ == '__main__':
    print("GATEWAY STARTED on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)
