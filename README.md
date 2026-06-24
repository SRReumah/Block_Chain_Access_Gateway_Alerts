# 🛡️ Blockchain Access Gateway with Real-Time Telegram Alerts

**A network security system that automatically detects, blocks, records, and alerts on network attacks using blockchain.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Solidity ^0.8.0](https://img.shields.io/badge/Solidity-%5E0.8.0-lightgrey.svg)](https://docs.soliditylang.org/)

---

## ⚡ The Problem

Traditional network security has 3 critical weaknesses:
- 🐌 **Slow Response** – Attacks detected hours/days later
- 🔓 **Tamperable Records** – Blacklists can be secretly modified
- 👁️ **No Transparency** – Can't verify who blocked what

---

## ✅ Our Solution

- ⚡ **<50ms Detection** – Suricata IDS
- 🔒 **<200ms Blocking** – Automatic smart contract
- 📝 **100% Immutable** – Blockchain records
- 📱 **Instant Alerts** – Telegram notifications
- 🎯 **<500ms Total** – Attack to enforcement

---

## 🏗️ Architecture (5 Components)

```
1. SURICATA IDS → Detects attack (<50ms)
         ↓
2. MONITOR SCRIPT → Reads alert, calls contract
         ↓
3. SMART CONTRACT → Records IP on blockchain (<200ms)
         ↓
4. FLASK GATEWAY → Checks chain, denies blocked IP
         ↓
5. TELEGRAM BOT → Sends instant alert to admin
```

**Total: <500ms from attack to enforcement**

---

## 📊 Performance Results

| Metric | Result |
|--------|--------|
| Detection time | <50ms |
| Blocking time | <200ms |
| Total pipeline | <500ms |
| Immutability | 100% |
| False positives | 0% |

---

## 🚀 Quick Start

### Prerequisites
- Kali Linux (defender)
- Python 3.8+
- Node.js 14+

### Install
```bash
git clone https://github.com/SRReumah/Block_Chain_Access_Gateway_Alerts.git
cd Block_Chain_Access_Gateway_Alerts
npm install
pip install -r requirements.txt
```

### Run (3 Terminals)
```bash
# Terminal 1
npx hardhat node

# Terminal 2
npx hardhat run scripts/deploy.js --network localhost
sudo python3 src/monitor.py

# Terminal 3
python3 src/gateway.py
```

### Test
```bash
nmap -sS 172.16.32.119
```

---

## 📚 Documentation

- [Quick Start](./docs/QUICK_START.md)
- [Kali Setup Guide](./docs/SETUP_KALI.md)
- [Usage Guide](./docs/USAGE.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)
- [Future Roadmap](./docs/FUTURE_ROADMAP.md)
- [Windows Setup Guide](./docs/SETUP_WINDOWS.md)
---

## 🔮 Future Roadmap

- [ ] Deploy to Ethereum mainnet
- [ ] ML-based anomaly detection
- [ ] Web dashboard for analytics
- [ ] Multi-signature authorization

---

## 👥 Authors

- **Aagama AR**
- **Sherin Rajan Reumah**

**Project Guide:** Dr. Amit Kumar Roy, IIIT Kottayam

---

## 📄 License

MIT License – see [LICENSE](./LICENSE) file

---

**⭐ If useful, please star this repo!**
