# Troubleshooting

## Challenge 1: Network Traffic Noise

**Problem:** Suricata picks up too much normal traffic

**Solution:**
- Filter monitor to detect only nmap scans
- Add threshold rules (5+ packets in 10 seconds)
- Edit `config/suricata/local.rules` with specific signatures

---

## Challenge 2: Telegram Unreachable

**Problem:** Telegram API blocked in lab network

**Solution:**
- System automatically falls back to console alerts
- Full alert details shown in monitor terminal
- On unrestricted network, Telegram works perfectly

---

## Challenge 3: Chain Resets on Restart

**Problem:** Hardhat loses blockchain data when node restarts

**Solution:**
- Re-deploy contract after restart: `npx hardhat run src/scripts/deploy.js --network localhost`
- Update contract address in `.env`
- Restart monitor and gateway
- For production, use persistent blockchain (mainnet or testnet)

---

## Issue: Suricata Not Detecting Attacks

**Check:**
1. Rules are loaded: `suricatectl update-rules`
2. Correct interface: `ip a` and update in `/etc/suricata/suricata.yaml`
3. Eve.json has alerts: `sudo tail -f /var/log/suricata/eve.json`

---

## Issue: Contract Not Found

**Solution:**
1. Re-deploy: `npx hardhat run src/scripts/deploy.js --network localhost`
2. Copy new address to `.env`
3. Restart all components

---

## Issue: Gateway Returns 500 Error

**Check:**
1. Hardhat node is running
2. Contract address in `src/gateway.py` matches `.env`
3. Web3.py connection: `python3 -c "from web3 import Web3; print(Web3.isConnected())"`

---

## Issue: Permission Denied on Suricata

**Solution:**
```bash
sudo python3 src/monitor.py
sudo usermod -a -G adm $USER
```

Log out and back in for group changes.

---

For more help, check [USAGE.md](./USAGE.md) or create a GitHub issue.
