# Quick Start (5 Minutes)

Get the system running in 5 minutes.

## Prerequisites
- Kali Linux (defender machine)
- Python 3.8+
- Node.js 14+
- nmap

## Step 1: Clone Repository
```bash
git clone https://github.com/SRReumah/Block_Chain_Access_Gateway_Alerts.git
cd Block_Chain_Access_Gateway_Alerts
```

## Step 2: Install Dependencies
```bash
npm install
pip install -r requirements.txt
cp .env.example .env
```

## Step 3: Configure Environment (Optional)
Edit `.env` and add Telegram bot token if you want notifications.

## Step 4: Run System (Open 3 Terminals)

**Terminal 1 – Start Blockchain:**
```bash
npx hardhat node
```

**Terminal 2 – Deploy & Monitor:**
```bash
npx hardhat run src/scripts/deploy.js --network localhost
sudo python3 src/monitor.py
```

**Terminal 3 – Start Gateway:**
```bash
python3 src/gateway.py
```

## Step 5: Test
From attacker machine:
```bash
nmap -sS 172.16.32.119 -p 1-100
```

**Watch:**
- ✅ Attack detected in monitor terminal
- ✅ IP blocked on blockchain
- ✅ Telegram alert (if configured)
- ✅ Gateway denies access

---

For detailed setup, see [SETUP_KALI.md](./SETUP_KALI.md)
