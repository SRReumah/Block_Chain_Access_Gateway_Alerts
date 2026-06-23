# Usage Guide

How to operate the Blockchain Access Gateway once it's installed and running.

---

## 🎯 System Overview

The system has three main components running in parallel:

1. **Hardhat node** – Blockchain for recording blocked IPs
2. **Monitor** – Watches Suricata alerts and blocks attackers
3. **Gateway** – HTTP service that enforces blocks

All three must be running together.

---

## 🚀 Starting the System

### Step 1: Start Hardhat node (Terminal 1)
```bash
cd ~/projects/Block_Chain_Access_Gateway_Alerts
npx hardhat node
```

Expected output:
```
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts:
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cFfb92266 (10000 ETH)
Account #1: 0x70997970C51812e339D9B73b0245ad59c36A2fF5 (10000 ETH)
...
```

### Step 2: Deploy contract (Terminal 2)
```bash
cd ~/projects/Block_Chain_Access_Gateway_Alerts
source venv/bin/activate
npx hardhat run scripts/deploy.js --network localhost
```

Expected output:
```
Deploying Blocklist contract...
Blocklist deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

### Step 3: Start the Monitor (Terminal 3)
```bash
cd ~/projects/Block_Chain_Access_Gateway_Alerts
source venv/bin/activate
sudo python3 monitor.py
```

Expected output:
```
KALI DEFENDER STARTED - watching for attacks...
Monitoring Suricata events at: /var/log/suricata/eve.json
```

### Step 4: Start the Gateway (Terminal 4)
```bash
cd ~/projects/Block_Chain_Access_Gateway_Alerts
source venv/bin/activate
python3 gateway.py
```

Expected output:
```
GATEWAY STARTED on http://0.0.0.0:8080
 * Serving Flask app 'gateway'
 * Debug mode: off
```

---

## 🧪 Testing the System

### Test 1: Normal access (IP not blocked)

From any machine on the network, try accessing the gateway:
```bash
curl http://172.16.32.119:8080/
```

Expected response:
```
ACCESS ALLOWED - Your IP 172.16.32.209 is clean!
```

### Test 2: Trigger an attack

From the attacker machine (Windows or another Linux box):
```bash
nmap -sS 172.16.32.119 -p 1-100
```

Watch the terminals:

**Monitor terminal (Terminal 3):**
```
=================================
*** ATTACK DETECTED ***
Attacker IP  : 172.16.32.209
Attack type  : NMAP SYN Scan Detected
Category     : ET INFO Spotiry P2P Client
Severity     : 3
Target       : 172.16.32.119:54 (TCP)
Detected at  : 2026-06-18 01:36:53
Action       : recording on the blockchain ...
=================================

IP 172.16.32.209 recorded on-chain
TX hash: a63f045201143a63cef5d53b81c805bce9ada8331b84efcbbed09bbd34e85a

[i] Telegram unreachable - full alert is shown above in this terminal.
```

**Gateway terminal (Terminal 4):**
```
172.16.32.209 - - [18/Jun/2026 01:36:55] "GET / HTTP/1.1" 403 FORBIDDEN
172.16.32.209 - - [18/Jun/2026 01:36:56] "GET / HTTP/1.1" 403 FORBIDDEN
```

### Test 3: Verify block is enforced

Try accessing from the attacker machine again:
```bash
curl http://172.16.32.119:8080/
```

Expected response:
```
ACCESS DENIED - Your IP 172.16.32.209 is blocked!
```

### Test 4: Check blocklist on chain

```bash
curl http://172.16.32.119:8080/blocked
```

Expected response:
```json
{
  "blocked_ips": [
    "172.16.32.209",
    "172.16.32.38"
  ]
}
```

---

## 📊 Monitor Commands & Signals

### Check monitor status
The monitor runs indefinitely. To stop it:
```bash
# In the monitor terminal, press Ctrl+C
```

The monitor logs to `monitor.log`:
```bash
tail -f monitor.log
```

### Monitor output format

When an attack is detected, you'll see:
```
=================================
*** ATTACK DETECTED ***
Attacker IP  : 172.16.32.209         # Source IP
Attack type  : NMAP SYN Scan Detected # Suricata signature
Category     : ET INFO Spotiry P2P    # Alert category
Severity     : 3                      # Severity (1-3, higher = more severe)
Target       : 172.16.32.119:54       # Victim IP:port
Detected at  : 2026-06-18 01:36:53   # Timestamp
Action       : recording on blockchain... # What the system is doing
=================================

IP 172.16.32.209 recorded on-chain
TX hash: a63f0452...                  # Blockchain transaction ID
```

---

## 🌐 Gateway API Reference

### GET `/` – Health check
```bash
curl http://172.16.32.119:8080/
```

Returns:
```
ACCESS ALLOWED - Your IP <IP> is clean!
```
or
```
ACCESS DENIED - Your IP <IP> is blocked!
```

### GET `/health` – Server status
```bash
curl http://172.16.32.119:8080/health
```

Returns:
```json
{
  "status": "running",
  "uptime_seconds": 1234,
  "connected_to_contract": true
}
```

### GET `/blocked` – List all blocked IPs
```bash
curl http://172.16.32.119:8080/blocked
```

Returns:
```json
{
  "blocked_ips": [
    "172.16.32.209",
    "172.16.32.38",
    "192.168.1.100"
  ],
  "total": 3
}
```

### GET `/blocked/<ip>` – Check specific IP
```bash
curl http://172.16.32.119:8080/blocked/172.16.32.209
```

Returns:
```json
{
  "ip": "172.16.32.209",
  "is_blocked": true
}
```

---

## 📝 Log Files

### Suricata events
```bash
# Real-time Suricata alerts
sudo tail -f /var/log/suricata/eve.json | jq '.'
```

### Monitor logs
```bash
# Monitor activity
tail -f monitor.log
```

### Gateway logs
```bash
# Gateway requests
tail -f gateway.log
```

### Hardhat node logs
Check Terminal 1 where Hardhat is running for blockchain transactions.

---

## ⚙️ Configuration

### Change detection threshold

Edit `monitor.py`:
```python
# Line ~45: Only block on multiple events in time window
ALERT_THRESHOLD = 5  # Number of alerts before blocking
TIME_WINDOW = 10     # Time window in seconds
```

### Change gateway port

Edit `gateway.py`:
```python
FLASK_PORT = 8080  # Change to your desired port
```

Or in `.env`:
```env
FLASK_PORT=9090
```

### Change Telegram settings

In `.env`:
```env
TELEGRAM_BOT_TOKEN=your_new_token
TELEGRAM_CHAT_ID=your_new_chat_id
```

Then restart monitor:
```bash
Ctrl+C in monitor terminal
python3 monitor.py
```

---

## 🚨 Emergency Stop

### Stop all components
```bash
# Terminal with monitor
Ctrl+C

# Terminal with gateway
Ctrl+C

# Terminal with Hardhat
Ctrl+C
```

### Emergency block removal
If you need to unblock an IP, you must redeploy the contract. In a production system, you'd have an "unblock" function in the contract.

Current workaround:
```bash
# Restart Hardhat, deploy fresh contract
npx hardhat node
npx hardhat run scripts/deploy.js --network localhost
# Update .env with new contract address
# Restart monitor and gateway
```

---

## 🔍 Monitoring in Real-Time

### Watch all events simultaneously
```bash
# Terminal 1: Suricata events
sudo tail -f /var/log/suricata/eve.json | jq '.alert | select(.action=="alert")'

# Terminal 2: Monitor output
tail -f monitor.log

# Terminal 3: Gateway requests
tail -f gateway.log
```

### Test with persistent nmap scan
```bash
# Attacker machine: Scan every 10 seconds for 2 minutes
for i in {1..12}; do 
  nmap -sS 172.16.32.119 -p 1-100
  sleep 10
done
```

Watch multiple IPs get blocked in real-time.

---

## 📊 Performance Monitoring

### Check contract calls
The Hardhat node logs all contract interactions:
```bash
# Look for contract calls in Hardhat terminal output
# You'll see gas usage and transaction details
```

### Measure response time
```bash
# From attacker machine
time curl http://172.16.32.119:8080/
```

Expected response time: <100ms

---

## 🤔 Common Questions

### Q: Can I access the gateway while it's running?
Yes, the gateway is designed to accept legitimate traffic. Only blocked IPs are denied.

### Q: What if Hardhat node crashes?
Restart it and redeploy the contract. The monitor will reconnect automatically.

### Q: Can I modify the Solidity contract while running?
Yes, but you need to redeploy:
1. Edit `contracts/Blocklist.sol`
2. Restart Hardhat
3. Run `npx hardhat run scripts/deploy.js --network localhost`
4. Update `.env` with new contract address
5. Restart monitor and gateway

### Q: How many IPs can the contract store?
On a local node, no practical limit. On mainnet, limited by gas costs (~$0.10-0.50 per block).

### Q: Can I whitelist IPs?
Currently, the contract only has a blocklist. To whitelist, you'd need to modify the smart contract to check an allowlist first.

---

## 📚 Next Steps

1. **Read [ARCHITECTURE.md](./ARCHITECTURE.md)** to understand how everything connects
2. **Customize detection rules** in Suricata (see SETUP.md)
3. **Extend the contract** with additional features (unblocking, whitelisting)
4. **Deploy to testnet** (Sepolia) instead of local Hardhat

---

## 📞 Need Help?

- Check `/var/log/suricata/suricata.log` for Suricata errors
- Check terminal output for Python errors
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
