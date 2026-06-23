# System Architecture

Technical overview of how the Blockchain Access Gateway works internally.

---

## 🎯 Design Principles

1. **Automatic** – Zero human intervention in attack-to-block pipeline
2. **Immutable** – Records on blockchain can't be altered or deleted
3. **Transparent** – All actions are verifiable and auditable
4. **Real-time** – Response in milliseconds, not minutes
5. **Decentralized** – No single point of failure

---

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ATTACKER                             │
│              Windows / Linux / Any OS                   │
│                 nmap -sS scan                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    DEFENDER                             │
│                   Kali Linux                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  1. DETECTION LAYER (Suricata IDS)              │  │
│  │  - Monitors network traffic                      │  │
│  │  - Detects SYN port scan pattern                │  │
│  │  - Writes alert to eve.json log                 │  │
│  └──────────────────────────────────────────────────┘  │
│                     │                                   │
│                     ▼ (50ms)                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │  2. DECISION LAYER (Python Monitor)             │  │
│  │  - Reads eve.json in real-time                  │  │
│  │  - Extracts attacker IP from alert              │  │
│  │  - Calls smart contract blockIP() function      │  │
│  └──────────────────────────────────────────────────┘  │
│                     │                                   │
│                     ▼ (200ms)                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │  3. BLOCKCHAIN LAYER (Hardhat Local Node)       │  │
│  │  - Smart contract records IP (Solidity)         │  │
│  │  - Transaction committed to chain               │  │
│  │  - 100% immutable, can't be modified            │  │
│  └──────────────────────────────────────────────────┘  │
│                     │                                   │
│                     ▼ (instant)                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  4. NOTIFICATION LAYER (Telegram Bot)           │  │
│  │  - Sends real-time alert to admin               │  │
│  │  - Shows IP, attack type, timestamp             │  │
│  └──────────────────────────────────────────────────┘  │
│                     │                                   │
│                     ▼ (instant)                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  5. ENFORCEMENT LAYER (Flask Gateway)           │  │
│  │  - Web service on port 8080                     │  │
│  │  - Checks each request against blocklist        │  │
│  │  - Denies access from blocked IPs               │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  "ACCESS DENIED - Your IP is blocked!"                │
└─────────────────────────────────────────────────────────┘
```

**Total pipeline: <500ms from attack to enforcement**

---

## 🔍 Detailed Components

### 1. Detection Layer: Suricata IDS

**Role:** Monitor network traffic and identify attacks

**How it works:**
```
Network Interface (eth0)
        ↓
Suricata packet capture (AF_PACKET)
        ↓
Pattern matching engine
        ↓
Match: 5+ SYN packets to different ports in 10 seconds
        ↓
Trigger alert rule
        ↓
Write to /var/log/suricata/eve.json (JSON format)
```

**Custom Suricata Rule:**
```
alert tcp any any -> any any (
  msg:"NMAP SYN Scan Detected";
  flags:S;                           # SYN flag
  threshold: type both,
    track by_src,
    count 5,                         # 5+ packets
    seconds 10;                      # in 10 seconds
  sid:1000001;
  rev:1;
)
```

**Alert JSON format:**
```json
{
  "timestamp": "2026-06-18T01:36:53.123456+0000",
  "alert": {
    "action": "alert",
    "gid": 1,
    "signature_id": 1000001,
    "signature": "NMAP SYN Scan Detected",
    "category": "Attempted Reconnaissance",
    "severity": 3
  },
  "src_ip": "172.16.32.209",
  "dest_ip": "172.16.32.119",
  "proto": "TCP",
  "tcp": {
    "src_port": 54321,
    "dest_port": 80,
    "flags": "S"
  }
}
```

---

### 2. Decision Layer: Python Monitor

**File:** `monitor.py`

**Role:** Bridge between detection and blockchain

**Workflow:**
```python
while True:
    # 1. Tail eve.json log
    for alert in read_new_alerts(eve_log):
        
        # 2. Filter for our signature
        if "NMAP SYN Scan" in alert['alert']['signature']:
            
            # 3. Extract attacker IP
            attacker_ip = alert['src_ip']
            
            # 4. Call smart contract
            tx_hash = contract.functions.blockIP(attacker_ip).transact(
                {'from': account, 'gas': 100000}
            )
            
            # 5. Send Telegram notification
            send_telegram_alert(attacker_ip, alert)
            
            # 6. Log the action
            print(f"IP {attacker_ip} blocked on-chain")
```

**Key Code:**
```python
# Read logs efficiently (like `tail -f`)
def read_new_alerts(log_file):
    with open(log_file, 'r') as f:
        # Seek to end on first run
        f.seek(0, 2)  # Go to end of file
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.01)  # Wait 10ms for new data
                continue
            
            try:
                alert = json.loads(line)
                yield alert
            except:
                pass

# Call smart contract
def block_ip_on_chain(ip):
    tx = contract.functions.blockIP(ip).transact(
        {'from': w3.eth.accounts[0]}
    )
    w3.eth.wait_for_transaction_receipt(tx)
    return tx.hex()
```

---

### 3. Blockchain Layer: Smart Contract

**File:** `contracts/Blocklist.sol`

**Language:** Solidity (Ethereum smart contracts)

**Role:** Immutable record of all blocked IPs

**Contract Code (simplified):**
```solidity
pragma solidity ^0.8.0;

contract Blocklist {
    // Mapping: IP address → blocked (true/false)
    mapping(string => bool) public blockedAddresses;
    
    // Array of all blocked IPs
    string[] public blockedIPs;
    
    // Event emitted when IP is blocked
    event IPBlocked(string indexed ip, uint256 timestamp);
    
    // Block an IP address
    function blockIP(string memory ip) public {
        require(!blockedAddresses[ip], "IP already blocked");
        
        blockedAddresses[ip] = true;
        blockedIPs.push(ip);
        
        emit IPBlocked(ip, block.timestamp);
    }
    
    // Check if IP is blocked
    function isBlocked(string memory ip) public view returns (bool) {
        return blockedAddresses[ip];
    }
    
    // Get all blocked IPs
    function getAllBlocked() public view returns (string[] memory) {
        return blockedIPs;
    }
    
    // Get count of blocked IPs
    function getBlockCount() public view returns (uint256) {
        return blockedIPs.length;
    }
}
```

**Why Blockchain?**
- ✅ **Immutable** – Once recorded, can't be changed
- ✅ **Transparent** – Anyone can read the blocklist
- ✅ **Decentralized** – No single admin can secretly modify
- ✅ **Auditable** – Full history of every block with timestamp
- ✅ **Tamper-evident** – Hash chain ensures no data modification

**Deployment:**
```javascript
async function main() {
    const Blocklist = await ethers.getContractFactory("Blocklist");
    const contract = await Blocklist.deploy();
    await contract.deployed();
    console.log("Blocklist deployed to:", contract.address);
}

main().catch(error => {
    console.error(error);
    process.exitCode = 1;
});
```

---

### 4. Notification Layer: Telegram Bot

**Role:** Real-time alert to administrator

**How it works:**
```
Event: IP blocked
    ↓
Python code calls Telegram API
    ↓
Message sent to bot
    ↓
Admin receives notification on phone/desktop
```

**Alert message format:**
```
🚨 CRITICAL ALERT: ATTACK DETECTED 🚨

Source IP: 172.16.32.209
Signature: ET INFO Spotiry P2P Client
Category: Attempted Reconnaissance
Severity: 3
Target: 172.16.32.119:54 (TCP)
Detected: 2026-06-18 01:36:53

Action: Blocking IP via Smart Contract
✅ IP 172.16.32.209 blocked
📝 TX: 9b757915f050332c89a0b32fa43aed4d7e5eee90...

Blocklist Dashboard: http://172.16.32.119:8080/blocked
```

**Python code:**
```python
import requests

def send_telegram_alert(ip, attack_info):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    message = f"""
🚨 ATTACK DETECTED 🚨
IP: {ip}
Type: {attack_info['alert']['signature']}
Time: {attack_info['timestamp']}
    """
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}
    
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        print(f"Telegram unreachable: {e}")
        print("Alert shown in console instead")
```

---

### 5. Enforcement Layer: Flask Gateway

**File:** `gateway.py`

**Role:** HTTP API that blocks requests from banned IPs

**How it works:**
```
User request to gateway
    ↓
Extract user's IP from request
    ↓
Query smart contract: isBlocked(user_ip)?
    ↓
If blocked: Return 403 Forbidden
If clean: Return 200 OK + content
```

**Flask code (simplified):**
```python
from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract = load_contract()

@app.route('/')
def home():
    user_ip = request.remote_addr
    
    # Check if IP is blocked
    is_blocked = contract.functions.isBlocked(user_ip).call()
    
    if is_blocked:
        return f"ACCESS DENIED - Your IP {user_ip} is blocked!", 403
    else:
        return f"ACCESS ALLOWED - Your IP {user_ip} is clean!", 200

@app.route('/blocked')
def get_blocklist():
    blocked_ips = contract.functions.getAllBlocked().call()
    return jsonify({'blocked_ips': blocked_ips})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

## 📊 Data Flow Diagram

```
TIME PROGRESSION →

0ms:   Attacker sends SYN packet
       │
       ▼
50ms:  Suricata IDS detects pattern
       Writes to eve.json
       │
       ▼
100ms: Monitor reads alert
       │
       ▼
200ms: Monitor calls contract.blockIP()
       Transaction included in block
       │
       ▼
300ms: Blockchain confirms transaction
       │
       ▼
500ms: Gateway enforces block
       (Blocks next request from attacker)
```

---

## 🔄 Sequence Diagram

```
Attacker        Suricata        Monitor          Contract        Gateway
   │                │                │                │               │
   │─────SYN pkts──→│                │                │               │
   │                │                │                │               │
   │                │────alert───────→                │               │
   │                │              (50ms)              │               │
   │                │                │                │               │
   │                │                │──blockIP()────→│               │
   │                │                │              (100ms)            │
   │                │                │                │               │
   │                │                │                ├─TX hash──────→│
   │                │                │              (200ms)          │
   │                │                │                │               │
   │                │◄───Telegram alert─(msg: blocked)               │
   │                │              (instant)          │               │
   │                │                │                │               │
   │───request────→ │                │                │───check IP───→│
   │                │                │                │              │
   │                │                │                │◄─is_blocked──│
   │                │                │                │              │
   │◄──403 Blocked──────────────────────────────────────             │
   │
```

---

## 🏛️ Data Structures

### Suricata Eve Alert
```json
{
  "timestamp": "ISO-8601",
  "alert": {
    "action": "alert",
    "signature": "Rule message",
    "severity": 1-3
  },
  "src_ip": "attacker IP",
  "dest_ip": "victim IP",
  "tcp": { "src_port": N, "dest_port": N }
}
```

### Smart Contract State
```solidity
blockedAddresses: {
  "172.16.32.209" => true,
  "172.16.32.38"  => true,
  "192.168.1.100" => true
}

blockedIPs: [
  "172.16.32.209",
  "172.16.32.38",
  "192.168.1.100"
]
```

### Gateway Response
```json
{
  "blocked_ips": ["172.16.32.209", "172.16.32.38"],
  "total": 2,
  "timestamp": "2026-06-18T01:36:53Z"
}
```

---

## ⚡ Performance Analysis

| Component | Time | Bottleneck |
|-----------|------|-----------|
| Detection (Suricata) | 50ms | Network packet processing |
| Decision (Monitor) | 50ms | File I/O (eve.json read) |
| Blockchain (Hardhat) | 200ms | Transaction confirmation |
| Notification (Telegram) | <100ms | Network latency |
| **Total** | **~500ms** | Blockchain confirmation |

**Optimization opportunities:**
- Move to mainnet (higher latency but more decentralized)
- Use Web3.py subscription for real-time events (vs polling)
- Batch multiple IPs per transaction (gas efficiency)
- Use Layer 2 rollups (lower latency + cost)

---

## 🔐 Security Considerations

### What we protect against:
- ✅ Tampering with blocklist (blockchain immutability)
- ✅ Unauthorized unblocking (no unblock function)
- ✅ Delayed detection (automatic Suricata rules)
- ✅ Missing audit trail (on-chain records)

### What we don't protect against:
- ❌ Compromise of Hardhat private key (move to mainnet)
- ❌ Suricata rule bypass (add more detection rules)
- ❌ Monitor.py exploitation (run with minimal privileges)
- ❌ Gateway DoS (add rate limiting)

---

## 🚀 Scalability

### Local Hardhat Node
- Unlimited IPs (memory limit)
- Instant block production
- No gas costs (local only)
- Perfect for testing

### Ethereum Mainnet
- ~1 million IPs per $1000 (gas costs)
- 12-15 seconds per block
- Decentralized and censorship-resistant
- Suitable for production

### Layer 2 Rollups (Arbitrum, Optimism)
- ~10x cheaper than mainnet
- 2-5 second finality
- Better UX than mainnet
- Recommended for scale

---

## 🔮 Future Architecture

```
Current (Proof of Concept)
└── Hardhat Local Node
    └── Single Machine

Future (Production)
└── Ethereum L2 Rollup (e.g., Arbitrum)
    ├── Multi-signature authorization
    ├── Whitelist contract (complement to blocklist)
    ├── Decentralized governance (DAO)
    └── Cross-chain blocklist sharing
```

---

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| `monitor.py` | Detection → Blockchain bridge |
| `gateway.py` | HTTP enforcement layer |
| `contracts/Blocklist.sol` | Immutable blocklist record |
| `scripts/deploy.js` | Contract deployment |
| `/var/log/suricata/eve.json` | Raw detection events |

---

## 🎓 Learning Resources

- **Suricata:** https://suricata.io/
- **Solidity:** https://docs.soliditylang.org/
- **Hardhat:** https://hardhat.org/
- **Web3.py:** https://web3py.readthedocs.io/
- **Ethereum:** https://ethereum.org/en/developers/

---

This architecture balances **security** (immutable blockchain), **speed** (<500ms), and **transparency** (auditable records) to solve the traditional firewall's problems.
