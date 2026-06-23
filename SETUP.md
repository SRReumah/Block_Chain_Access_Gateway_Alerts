# Installation & Setup Guide

Complete step-by-step instructions to get the Blockchain Access Gateway running on your system.

---

## 📋 Requirements

### Hardware
- **Defender machine:** Kali Linux (VM or physical)
- **Attacker machine:** Windows 10/11 or another Linux box (same network as defender)
- **Minimum RAM:** 4GB per machine
- **Disk space:** 10GB for Kali Linux + tools

### Software
- **Kali Linux** with internet access
- **Python 3.8+**
- **Node.js 14+** (for Hardhat & Ethereum development)
- **npm** (comes with Node.js)
- **nmap 7.8+** (for testing)
- **curl** or **wget** (for downloading)

---

## 🚀 Installation Steps

### Phase 1: Prepare Kali Linux (Defender)

#### 1.1 Update system packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### 1.2 Install Python and pip
```bash
sudo apt-get install -y python3 python3-pip python3-venv
python3 --version  # Should be 3.8 or higher
```

#### 1.3 Install Node.js and npm
```bash
# Using Node Version Manager (nvm) is recommended
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18
node --version  # Should be v18.x.x
npm --version   # Should be 9.x.x or higher
```

Or install directly:
```bash
sudo apt-get install -y nodejs npm
```

#### 1.4 Install Suricata IDS
```bash
sudo apt-get install -y suricata

# Verify installation
suricata --version
```

#### 1.5 Configure Suricata for network monitoring
```bash
# Find your network interface (usually eth0 or wlan0)
ip a

# Edit Suricata config (replace eth0 with your interface)
sudo nano /etc/suricata/suricata.yaml
```

Look for the `af-packet:` section and ensure it's enabled:
```yaml
af-packet:
  - interface: eth0
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes
```

#### 1.6 Start Suricata service
```bash
sudo systemctl start suricata
sudo systemctl enable suricata  # Auto-start on boot
sudo systemctl status suricata  # Verify it's running
```

#### 1.7 Install Git
```bash
sudo apt-get install -y git
git --version
```

---

### Phase 2: Clone & Setup Project

#### 2.1 Clone the repository
```bash
# Navigate to a work directory
cd ~/projects  # Create if needed: mkdir -p ~/projects
cd projects

# Clone
git clone https://github.com/SRReumah/Block_Chain_Access_Gateway_Alerts.git
cd Block_Chain_Access_Gateway_Alerts
```

#### 2.2 Install Node.js dependencies
```bash
npm install
# This creates node_modules/ and installs Hardhat, ethers, etc.
```

#### 2.3 Create Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.4 Install Python dependencies
```bash
pip install -r requirements.txt
```

Expected packages:
- web3
- flask
- requests (for Telegram)
- python-telegram-bot

---

### Phase 3: Configure Environment Variables

#### 3.1 Create `.env` file
```bash
cp .env.example .env
nano .env
```

Fill in the following values:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Blockchain Configuration
HARDHAT_RPC_URL=http://127.0.0.1:8545
CONTRACT_ADDRESS=  # Leave empty for now; we'll fill after deployment

# Suricata Configuration
SURICATA_EVE_LOG=/var/log/suricata/eve.json
SURICATA_INTERFACE=eth0  # Change to your interface if different

# Flask Gateway Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=8080
FLASK_DEBUG=False
```

#### 3.2 Telegram Bot Setup (optional, for testing)
To use Telegram notifications:
1. Open Telegram and message [@BotFather](https://t.me/botfather)
2. Type `/newbot` and follow instructions
3. Copy the API token to `TELEGRAM_BOT_TOKEN` in `.env`
4. Get your chat ID:
   - Send a message to your bot
   - Visit `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
   - Find your `chat.id` and add it to `TELEGRAM_CHAT_ID`

---

### Phase 4: Deploy Smart Contract

#### 4.1 Start Hardhat local node (Terminal 1)
```bash
npx hardhat node
```

Output should show:
```
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/
```

**Keep this terminal open.**

#### 4.2 Deploy contract (Terminal 2, in project directory)
```bash
source venv/bin/activate
npx hardhat run scripts/deploy.js --network localhost
```

Output should show:
```
Deploying Blocklist contract...
Blocklist deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
```

#### 4.3 Update `.env` with contract address
Copy the contract address and add it to `.env`:
```env
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
```

---

### Phase 5: Configure Suricata Rules

#### 5.1 Add custom nmap detection rule
```bash
sudo nano /etc/suricata/rules/custom.rules
```

Add this rule:
```
alert tcp any any -> any any (msg:"NMAP SYN Scan Detected"; flags:S; threshold: type both, track by_src, count 5, seconds 10; sid:1000001; rev:1;)
```

#### 5.2 Reload Suricata to apply rules
```bash
sudo suricatectl update-rules
sudo systemctl restart suricata
```

---

### Phase 6: Test Suricata Alerts

#### 6.1 Verify Suricata is logging
```bash
sudo tail -f /var/log/suricata/eve.json | jq '.' | head -20
```

#### 6.2 Trigger a test alert (from attacker machine or same machine)
```bash
nmap -sS 127.0.0.1 -p 1-100
```

#### 6.3 Check logs again
```bash
sudo tail -f /var/log/suricata/eve.json | grep "NMAP"
```

You should see NMAP alerts appearing.

---

### Phase 7: Run the System

#### Terminal 1: Hardhat node (already running)
```bash
npx hardhat node
```

#### Terminal 2: Monitor (Reads Suricata alerts, calls contract)
```bash
source venv/bin/activate
sudo python3 monitor.py
```

Output:
```
KALI DEFENDER STARTED - watching for attacks...
```

#### Terminal 3: Flask Gateway (Enforces blocks)
```bash
source venv/bin/activate
python3 gateway.py
```

Output:
```
GATEWAY STARTED on http://0.0.0.0:8080
Serving Flask app...
```

#### Terminal 4: Test from Attacker
```bash
nmap -sS 172.16.32.119  # Replace with defender's IP
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# Check Suricata is running
sudo systemctl status suricata

# Check Hardhat node is reachable
curl http://127.0.0.1:8545 -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":67}'

# Check gateway is running
curl http://127.0.0.1:8080/health

# Check contract was deployed
grep "deployed to:" hardhat.log
```

---

## 🐛 Troubleshooting

### "Permission denied" for Suricata
```bash
# Run monitor with sudo
sudo python3 monitor.py
```

### "Cannot connect to Hardhat node"
```bash
# Verify Hardhat is running
curl http://127.0.0.1:8545
# Should return a JSON response
```

### "Suricata eve.json not found"
```bash
# Check log location
sudo find / -name "eve.json" 2>/dev/null
# Update path in monitor.py and .env
```

### "Telegram unreachable"
In lab networks, Telegram might be blocked. The system falls back to console alerts.

### "contract address mismatch"
Hardhat generates a new address each time it restarts. After restart:
1. Run `npx hardhat run scripts/deploy.js --network localhost`
2. Copy new address to `.env`
3. Restart monitor and gateway

---

## 📁 Folder Permissions

Ensure proper permissions for logs:
```bash
# Suricata logs directory
sudo usermod -a -G adm $USER
sudo usermod -a -G suricata $USER

# Your project directory
chmod 755 ~/projects/Block_Chain_Access_Gateway_Alerts
```

Log out and back in for group changes to take effect.

---

## 🎓 Next Steps

1. **Read [USAGE.md](./USAGE.md)** to learn how to operate the system
2. **Review [ARCHITECTURE.md](./ARCHITECTURE.md)** to understand the design
3. **Test the system** with nmap scans from the attacker machine
4. **Customize Suricata rules** for your specific detection needs

---

## 📞 Issues?

If you encounter problems:
1. Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. Review the logs:
   ```bash
   sudo tail -f /var/log/suricata/suricata.log
   tail -f monitor.log
   tail -f gateway.log
   ```
3. Open a [GitHub Issue](../../issues) with error messages and logs
