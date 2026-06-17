# Blockchain Access Gateway with Real-Time Telegram Alerts

A network-security system that **automatically detects, blocks, records, and alerts** on
network attacks. When an attacker scans the defender machine, Suricata detects it, a Python
monitor records the attacker's IP on a blockchain smart contract, a Telegram alert fires
instantly, and a gateway then denies that IP any further access — all in under half a second,
with no human in the loop.

> **How to describe it accurately:** This is a **hybrid** system. Detection and enforcement run
> on one machine (centralized); the **blocklist** is stored on a blockchain (decentralized and
> immutable). The blockchain itself is a **private/permissioned** chain (a single local Hardhat
> node). Say *"the record-keeping is decentralized and tamper-proof; the system overall is hybrid;
> the chain is private."* Do not call the whole system "fully decentralized."

---

## Who does what

This is a **two-person, two-machine** project on the **same network**:

| Person | Machine | Role | Setup file |
|--------|---------|------|------------|
| Friend | **Kali Linux** | The **defender / victim**. Runs the *entire* system. | `SETUP_KALI.md` |
| You | **Windows** | The **attacker** (simulated). Only runs `nmap`. | `SETUP_WINDOWS.md` |

Nothing from this project is installed on Windows except Nmap.

---

## How it works (the 5-step flow)

```
   WINDOWS (Attacker)                 KALI LINUX (Defender - runs everything)
   172.16.197.x                       172.16.197.21
        |                                   |
        |   1.  nmap -sS 172.16.197.21       |
        |  ------------------------------->  |  2. Suricata detects the scan
        |                                    |  3. monitor.py records the IP on the blockchain
        |                                    |     + sends a Telegram alert to the admin
        |                                    |
        |   5.  curl http://...:8080         |
        |  ------------------------------->  |  4./6. gateway.py checks the blocklist
        |   <----  ACCESS DENIED  ---------  |       and denies the blocked IP
```

1. **Suricata** (intrusion-detection system) watches all traffic into Kali. A custom rule fires
   when it sees the rapid SYN packets of an nmap port scan, writing an alert to
   `/var/log/suricata/eve.json`.
2. **monitor.py** continuously reads that log. On each new alert it pulls out the attacker's IP.
3. **The smart contract** (Solidity, on a local Hardhat blockchain) records that IP permanently
   and immutably.
4. **Telegram bot** sends an instant alert to the admin's phone.
5. **gateway.py** (a Flask web service) checks every incoming connection against the on-chain
   blocklist and returns **Access Denied** to blocked IPs.

---

## What the attacker is actually doing

A port scan (`nmap`) is **reconnaissance** — the first step of a real attack, where the attacker
probes which ports/services are open to find a way in. The project's contribution is **not** about
protecting any specific data; it is about **detecting that scan and blocking the attacker early,
with a tamper-proof record**, before any real intrusion can happen. The attacker can be *any*
device on the network — Windows is just what we used to simulate one.

---

## Files in this project

```
blockchain-access-gateway/
├── contracts/
│   └── Blocklist.sol          # the smart contract (on-chain blocklist)
├── scripts/
│   └── deploy.js              # deploys the contract to the local chain
├── suricata/
│   ├── local.rules            # the custom Suricata detection rule
│   └── SETTINGS_TO_CHANGE.txt # what to edit in suricata.yaml
├── monitor.py                 # reads alerts -> records IP on-chain + Telegram
├── gateway.py                 # web service that denies blocked IPs
├── contract_address.py        # paste the deployed contract address here
├── hardhat.config.js          # Hardhat (blockchain) config
├── package.json               # Node/Hardhat dependencies
├── requirements.txt           # Python dependencies
├── README.md                  # this file
├── SETUP_KALI.md              # FRIEND: full Kali setup + run steps
├── SETUP_WINDOWS.md           # YOU: Windows attacker setup + run steps
└── VIVA_QA.md                 # questions professors may ask + answers
```

---

## Quick start

1. Friend follows **SETUP_KALI.md** end to end (installs everything, runs 5 terminals).
2. You follow **SETUP_WINDOWS.md** (install Nmap, run the scan, prove the block).
3. Read **VIVA_QA.md** together before the presentation.

**Do a full rehearsal once before the demo**, and record a screen video of a successful run as a
backup in case the live network misbehaves.

---

*Built with Suricata, Hardhat, Solidity, Python, Flask, web3.py, and the Telegram Bot API.*
