# SETUP — KALI LINUX (Friend / Defender)

You run the **entire** system. Follow these steps in order. By the end you will have
**5 terminals** open. Take it slowly — each step is simple.

---

## Part A — One-time installation (do this once, well before the demo)

Open a terminal and run:

```bash
# 1. Update and install the base tools
sudo apt update
sudo apt install -y nodejs npm suricata python3-pip curl

# 2. Install the Python libraries the project needs
pip install web3 requests flask --break-system-packages

# 3. Go into the project folder (wherever you unzipped it)
cd blockchain-access-gateway

# 4. Install the blockchain (Hardhat) dependencies
npm install
```

If `npm install` finishes without red ERROR lines, you're good. (Warnings are fine.)

---

## Part B — Configure Suricata (one-time)

```bash
# 1. Copy our custom detection rule into Suricata's rules folder
sudo cp suricata/local.rules /etc/suricata/rules/local.rules

# 2. Open the Suricata config
sudo nano /etc/suricata/suricata.yaml
```

Inside that file, make sure these two settings are correct (use Ctrl+W in nano to search):

```yaml
HOME_NET: "[172.16.197.0/24]"      # the network both machines are on

rule-files:
  - local.rules                     # add this line so our rule loads
```

Save (Ctrl+O, Enter) and exit (Ctrl+X). Then test the config:

```bash
sudo suricata -T -c /etc/suricata/suricata.yaml -v
```

You should see **"Configuration provided was successfully loaded."**

---

## Part C — Find your network details (do this once, note them down)

```bash
ip -br a
```

This lists your network interfaces. Note:
- Your **interface name** (e.g. `eth0`, `ens33`, or `enp0s3`) — you'll need it for Suricata.
- Your **IP address** — it should be on `172.16.197.x`. This is the defender IP.

If your IP is **not** on `172.16.197.x`, edit two things to match your real subnet:
- `HOME_NET` in `suricata.yaml`
- `KALI_IP` at the top of `monitor.py`

Also set up the Telegram bot (one-time):
1. On Telegram, message **@BotFather** → `/newbot` → follow prompts → copy the **bot token**.
2. Message **@userinfobot** → it replies with your **chat ID**.
3. Open `monitor.py` and paste both into `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

---

## Part D — Run the system (the 5 terminals)

Open a **new terminal for each step** and leave it running.

### Terminal 1 — Start the blockchain  (keep open)
```bash
cd blockchain-access-gateway
npx hardhat node
```
You'll see a list of 20 test accounts. Leave it running.

### Terminal 2 — Deploy the smart contract  (run once, then can close)
```bash
cd blockchain-access-gateway
npx hardhat run scripts/deploy.js --network localhost
```
It prints `Blocklist deployed to: 0x....`.
**Copy that address** and paste it into `contract_address.py` (replace the placeholder).

> Repeat Terminal 2 every time you restart Terminal 1 — the chain resets and the address changes.

### Terminal 3 — Start Suricata  (keep open)
```bash
sudo suricata -c /etc/suricata/suricata.yaml -i eth0     # use YOUR interface from Part C
```

### Terminal 4 — Start the monitor  (keep open)
```bash
cd blockchain-access-gateway
sudo python3 monitor.py
```
Wait for **"KALI DEFENDER STARTED - watching for attacks ..."**

### Terminal 5 — Start the gateway  (keep open)
```bash
cd blockchain-access-gateway
python3 gateway.py
```
Wait for **"GATEWAY STARTED on http://0.0.0.0:8080"**.

**Keep Terminals 1, 3, 4, 5 running during the whole demo.**

---

## Part E — Health check (run before the demo, in a spare terminal)

```bash
echo "=== 1. Blockchain node ==="
curl -s -X POST http://127.0.0.1:8545 -H "Content-Type: application/json" \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}' && echo
echo "=== 2. Contract deployed? ==="
python3 -c "from web3 import Web3; from contract_address import CONTRACT_ADDRESS; w3=Web3(Web3.HTTPProvider('http://127.0.0.1:8545')); print('deployed:', len(w3.eth.get_code(CONTRACT_ADDRESS))>2)"
echo "=== 3. Suricata running? ==="
pgrep -a suricata || echo "NOT running"
echo "=== 4. Gateway up? ==="
curl -s http://127.0.0.1:8080 && echo
```

If section 1 returns a result, section 2 says `deployed: True`, section 3 shows a process, and
section 4 says "ACCESS ALLOWED" — **everything is ready.**

To watch Suricata catch the attack live (optional, looks great in a demo):
```bash
sudo tail -f /var/log/suricata/eve.json | grep '"event_type":"alert"'
```

---

## If something goes wrong

| Problem | Fix |
|---------|-----|
| Monitor shows nothing during a scan | Wrong Suricata interface — re-run Terminal 3 with the correct `-i` name from `ip -br a` |
| "Cannot connect to Hardhat node!" | Terminal 1 isn't running — start it first |
| Contract errors in Terminal 4/5 | Wrong/old address in `contract_address.py` — re-deploy (Terminal 2) and re-paste |
| No Telegram message | Wrong bot token or chat ID in `monitor.py` |
| Gateway never says "Denied" | Both machines must be on the same `172.16.197.x` subnet; `ping` to confirm |
