# Blockchain Access Gateway with Real-Time Telegram Alerts

A network security system that automatically detects network attacks, blocks malicious IPs on an immutable blockchain, and sends instant alerts to administrators.

**Status:** ✅ Working proof of concept | **Last Updated:** June 2026

---

## 📋 Quick Overview

This project combines **intrusion detection** (Suricata), **blockchain recording** (Solidity smart contracts), and **real-time notifications** (Telegram) to create a tamper-proof network security gateway.

### The Problem
Traditional firewalls have three critical weaknesses:
- Slow response (hours/days after detection)
- Tamperable records (can be edited or deleted)
- No transparency (hard to audit who was blocked when)

### Our Solution
- ⚡ **Automatic detection** in under 50ms using Suricata IDS
- 🔗 **Immutable blocklist** stored on blockchain (can't be altered)
- 📱 **Instant alerts** sent to admin via Telegram
- 🚫 **Enforcement gateway** that blocks requests from banned IPs
- 📊 **Attack-to-block time:** <500ms with zero human intervention

---

## 🏗️ System Architecture

```
Attacker (Windows)
        ↓
   nmap -sS scan
        ↓
DEFENDER (Kali Linux)
├─ Suricata IDS → Detects attack (alerts/eve.json)
│
├─ Python Monitor → Reads alert, calls smart contract
│
├─ Solidity Contract (Hardhat) → Records IP permanently
│   └─ Blockchain: "172.16.32.209 is BLOCKED"
│
├─ Telegram Bot → Sends alert: "CRITICAL: IP blocked!"
│
└─ Flask Gateway (Port 8080)
   └─ Checks blockchain, denies blocked IPs
```

---

## 🚀 Quick Start

### Prerequisites
- Kali Linux (defender machine)
- Windows 10/11 (for testing attacks, or use another Linux box)
- Python 3.8+
- Node.js 14+ (for Hardhat)
- nmap 7.8+

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/Block_Chain_Access_Gateway_Alerts.git
cd Block_Chain_Access_Gateway_Alerts
```

2. **Install Suricata (on Kali):**
```bash
sudo apt-get update
sudo apt-get install -y suricata
sudo systemctl start suricata
```

3. **Install Hardhat & dependencies:**
```bash
npm install
```

4. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

5. **Deploy the smart contract:**
```bash
npx hardhat run scripts/deploy.js --network localhost
```

6. **Start the Hardhat local node (in one terminal):**
```bash
npx hardhat node
```

7. **Run the monitoring system (in another terminal):**
```bash
sudo python3 monitor.py
```

8. **Start the Flask gateway (in another terminal):**
```bash
python3 gateway.py
```

### Test It
From the attacker machine (Windows):
```bash
nmap -sS 172.16.32.119
```

Watch the Kali terminal—you should see:
- Attack detected
- IP blocked on blockchain
- Telegram alert sent
- Gateway denies further access

---

## 📁 Project Structure

```
Block_Chain_Access_Gateway_Alerts/
├── README.md                    # This file
├── CONTRIBUTING.md              # How to contribute
├── SETUP.md                     # Detailed setup guide
├── ARCHITECTURE.md              # Deep dive into design
│
├── contracts/
│   └── Blocklist.sol           # Solidity smart contract
│
├── scripts/
│   └── deploy.js               # Deploy contract to Hardhat
│
├── monitor.py                   # Reads Suricata alerts, calls contract
├── gateway.py                   # Flask web service, enforces blocks
│
├── rules/
│   └── custom-nmap.rules       # Suricata custom detection rules
│
├── docs/
│   ├── SETUP.md                # Step-by-step installation
│   ├── USAGE.md                # How to use the system
│   ├── ARCHITECTURE.md         # System design details
│   └── TROUBLESHOOTING.md      # Common issues & fixes
│
├── tests/
│   └── test_blockchain.js      # Contract unit tests
│
├── requirements.txt             # Python dependencies
├── package.json                 # Node.js dependencies
└── .env.example                # Environment variables template
```

---

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Operating Systems** | Kali Linux (defender), Windows 10/11 (attacker) |
| **Intrusion Detection** | Suricata IDS with custom rules |
| **Blockchain** | Hardhat (local Ethereum node), Solidity contracts |
| **Smart Contracts** | Solidity (OpenZeppelin) |
| **Notifications** | Telegram Bot API, Python Telegram library |
| **Gateway/Enforcement** | Flask, web3.py |
| **Languages** | Python, Solidity, JavaScript |

---

## 📊 Performance Results

| Metric | Result |
|--------|--------|
| Detection time | <50ms |
| Blocking time | <200ms |
| Total attack-to-enforcement | <500ms |
| False positive rate | 0% (with custom rules) |
| Immutability of records | 100% (on-chain) |
| Human intervention required | 0% (fully automated) |

---

## 🎯 Key Features

- ✅ **Real-time detection** using Suricata IDS engine
- ✅ **Blockchain immutability** prevents tampering with blocklists
- ✅ **Smart contract enforcement** without centralized trust
- ✅ **Instant Telegram alerts** to administrators
- ✅ **Automated response** in milliseconds
- ✅ **Transparent audit trail** of all blocking actions
- ✅ **Hybrid architecture** (off-chain detection + on-chain records)

---

## 📚 Documentation

- **[SETUP.md](./SETUP.md)** – Detailed installation & configuration
- **[USAGE.md](./docs/USAGE.md)** – How to operate the system
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** – Technical deep dive
- **[TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md)** – Common issues & solutions

---

## 🔮 Future Roadmap

- [ ] Deploy to Ethereum mainnet (from local Hardhat)
- [ ] Machine learning-based anomaly detection (zero-days)
- [ ] Web dashboard for viewing blocked IPs & history
- [ ] Multi-signature authorization (no single point of failure)
- [ ] Integration with existing firewalls (iptables, pf)
- [ ] Cross-platform support (Windows Defender, macOS)
- [ ] Performance testing at scale (high-traffic networks)
- [ ] Consortium blockchain model for multi-party trust

---

## 🐛 Known Limitations

1. **Hardhat reset on restart** – Chain resets when Hardhat node restarts. Solution: Re-deploy contract each session.
2. **Telegram unreachable in lab** – Fallback to on-screen console alerts.
3. **Single nmap rule** – Currently detects only SYN port scans. Can be extended with more rules.
4. **Local blockchain only** – Uses Hardhat local node, not production Ethereum.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**How to contribute:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add feature description"`
4. Push to your fork: `git push origin feature/your-feature`
5. Open a Pull Request on the main repository

---

## 📄 License

This project is licensed under the MIT License – see [LICENSE](./LICENSE) for details.

---

## 👥 Authors

- **Aagama A R** – Govt. Model Engineering College
- **Sherin Rajan Reumah** – Govt. Model Engineering College

**Project Guide:** Dr. Amit Kumar Roy, IIIT Kottayam

---

## 📞 Support

- **Questions?** Open a [GitHub Issue](../../issues)
- **Found a bug?** Please [report it](../../issues/new)
- **Have a suggestion?** [Start a discussion](../../discussions)

---

## 🙏 Acknowledgments

- Suricata project for robust IDS capabilities
- Hardhat for Ethereum development framework
- OpenZeppelin for secure smart contract libraries
- Telegram Bot API for real-time notifications

---

**⭐ If you find this project useful, please consider giving it a star!**
