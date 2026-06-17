# SETUP — WINDOWS (You / Attacker)

Your job is the easiest: you only **simulate the attacker**. You install one tool (Nmap) and
run two commands during the demo. Nothing else from the project runs on your machine.

---

## Part A — One-time installation

1. Download **Nmap** from the official site: https://nmap.org/download.html
   (Get the "Latest stable release self-installer" for Windows.)
2. Run the installer. **Keep the box "Npcap" checked** — Nmap needs it to send packets.
3. Finish the install (default options are fine).

To confirm it works, open **Command Prompt** (press Start, type `cmd`, Enter) and run:
```
nmap --version
```
You should see a version number (e.g. `Nmap version 7.9x`).

---

## Part B — Check the network (do this with your friend before the demo)

Both machines must be on the **same network** (`172.16.197.x`).

1. Find your Windows IP — in Command Prompt:
   ```
   ipconfig
   ```
   Look for **IPv4 Address** (should be `172.16.197.x`). Tell your friend this number.

2. Confirm you can reach the Kali machine:
   ```
   ping 172.16.197.21
   ```
   You should get replies. If it times out, the two machines aren't connected — fix the network
   (both VMs on the same Host-Only or Bridged adapter) before continuing.

---

## Part C — The demo (run these two commands when your friend's Kali side is ready)

### Step 1 — Launch the attack
```
nmap -sS 172.16.197.21 -p 1-100
```
What this means (in case you're asked):
- `nmap` — the scanning tool.
- `-sS` — a **SYN scan** (sends rapid connection requests to probe open ports). This is the
  pattern Suricata is trained to detect.
- `172.16.197.21` — the Kali defender you are "attacking."
- `-p 1-100` — scan ports 1 to 100 (enough packets to trigger the detection rule).

Within about a second, your friend's Kali screen will show **"ATTACK FROM <your-ip>"**, the
phone will get a **Telegram alert**, and your IP will be recorded on the blockchain.

### Step 2 — Prove you've been blocked
```
curl http://172.16.197.21:8080
```
Because you're now on the blocklist, the gateway replies:
```
ACCESS DENIED - Your IP <your-ip> is blocked!
```

(If `curl` isn't recognized, open the same address in a web browser instead:
`http://172.16.197.21:8080`)

---

## That's your entire part

Install Nmap, confirm the ping works, then run the scan and the curl during the demo. Everything
else happens automatically on the Kali side.

> Tip: if `ping` works but the scan shows "host seems down," add `-Pn` to the command:
> `nmap -sS -Pn 172.16.197.21 -p 1-100`
