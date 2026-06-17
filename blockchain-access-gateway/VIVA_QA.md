# VIVA Q&A — Be Ready for These

Read this together before the presentation. Answers are written in plain language so you can
say them in your own words. The most important ones are marked ⭐.

---

## The basics

**Q. Explain your project in one line.** ⭐
"When someone attacks our machine, we automatically detect it, permanently record the attacker
on a blockchain so the record can't be faked or deleted, instantly alert the admin on Telegram,
and block that attacker from any further access — all in under half a second, with no human
needed."

**Q. Walk us through how it works.** ⭐
"Windows runs an nmap scan on the Kali machine. Suricata detects the scan and writes an alert.
Our Python monitor reads that alert, takes the attacker's IP, records it on a blockchain smart
contract, and sends a Telegram alert. Our gateway then checks that blocklist and denies the
attacker any further access."

**Q. What are the main components / technologies?**
- Suricata — detects the attack (intrusion-detection system).
- monitor.py (Python) — the decision-maker that links detection to blocking.
- Smart contract (Solidity on Hardhat) — stores the blocklist permanently on the blockchain.
- Telegram Bot — alerts the admin.
- gateway.py (Flask + web3.py) — enforces the block (denies access).

---

## The decentralization / blockchain questions (most likely to be asked)

**Q. Is your project decentralized?** ⭐⭐
"The record-keeping is — the blocklist lives on a blockchain, so it's tamper-proof and
verifiable. But detection and enforcement run on a single machine, so the overall system is a
**hybrid**. And the blockchain itself is a **private** chain. We don't claim the whole system is
fully decentralized."

**Q. What type of blockchain is it — public, private, consortium, or hybrid?** ⭐
"The blockchain is **private (permissioned)** — it's a single local Hardhat node that only we can
access, with one key allowed to write. The overall *system* has a hybrid architecture. If we added
validator nodes from other parties it would become consortium; on a public testnet it would be
public."

**Q. What do you mean by 'the chain'?**
"'Chain' is short for blockchain. When we run `npx hardhat node`, it starts a small Ethereum-style
blockchain on the Kali machine — that running blockchain, which stores our blocked IPs, is 'the
chain.' It's local, not the public Ethereum network."

**Q. Why use a blockchain instead of a normal database?** ⭐
"A database can be silently edited or deleted by anyone with admin access — you can't prove the
record wasn't tampered with. A blockchain makes every entry permanent and verifiable, so we get a
tamper-proof audit trail of every block we made. That trust and immutability is the whole reason
we used blockchain."

**Q. If it's decentralized, why is there an 'admin'?** ⭐
"The admin is just the operator of the defender machine — the person who gets the Telegram alert.
The blockchain doesn't remove the operator; it makes the operator's actions auditable, so no one
can secretly tamper with the record of who was blocked."

**Q. What is a smart contract?**
"A program that runs on the blockchain. Ours is called Blocklist. It has functions to add a
blocked IP, check if an IP is blocked, and list all blocked IPs. Once deployed, it runs
automatically and its data can't be altered."

**Q. What is the consensus mechanism?**
"We use a local Hardhat development node, which is a single-node test blockchain — it doesn't run
real Proof-of-Work or Proof-of-Stake consensus. It gives us the immutability and smart-contract
behaviour we need for the demo. Real consensus would come into play if we deployed to a public or
consortium network, which is part of our future work."

---

## The attack questions

**Q. Can any device be the attacker, or only Windows?** ⭐
"Any device on the network. Our system blocks whatever IP Suricata flags as scanning it. We just
used a Windows machine to simulate the attacker for the demo."

**Q. What is the attacker actually trying to do? What do they want?** ⭐
"A port scan is reconnaissance — the first step of a real attack. The attacker is probing to find
which ports and services are open, so they can find a weakness to exploit later. Our project
catches them at this scanning stage and blocks them before they can go further."

**Q. What data on the Kali machine is the attacker after?**
"Our project isn't about protecting a specific piece of data — the Kali machine represents any
protected server. We focus on the defensive response: detecting the scan and blocking the attacker
early, rather than modelling stolen data."

**Q. What is nmap? What is a SYN scan?**
"Nmap is a network scanning tool. A SYN scan sends rapid 'SYN' connection requests to many ports
to find which are open, without completing the full connection — that rapid burst of SYN packets
is the pattern Suricata detects."

**Q. What if the attacker doesn't scan first?**
"Correct — our current rule targets port scans, the most common first step. Detecting other attack
types like brute-force or exploits would need extra rules or machine-learning detection, which is
in our future work."

---

## The technical detail questions

**Q. What is Suricata?**
"An open-source intrusion-detection system. It inspects network traffic against rules and raises
an alert when it sees something matching — in our case, an nmap scan."

**Q. How does Suricata know it's an attack?**
"We wrote a custom rule: if one source sends 20 or more SYN packets within 5 seconds, that's the
signature of a port scan, so Suricata raises an alert."

**Q. What is eve.json?**
"It's Suricata's log file where it writes events in JSON format. Our monitor reads new lines from
it to catch alerts as they happen."

**Q. How does the monitor talk to the blockchain?**
"Through the web3.py library, which sends a transaction to the Hardhat node over its RPC interface
(`http://127.0.0.1:8545`) calling the contract's `blockIP` function."

**Q. What is the private key in monitor.py for?**
"Every blockchain transaction must be signed by an account. The key signs our `blockIP`
transactions. We use Hardhat's built-in test account — fine for a local demo, never used for real
money."

**Q. What is Hardhat?**
"A development framework for Ethereum. It gives us a local test blockchain and tools to compile and
deploy our smart contract."

**Q. What is web3.py?**
"A Python library for talking to an Ethereum blockchain — we use it in both the monitor (to write)
and the gateway (to read)."

**Q. What is the gateway and why Flask?**
"The gateway is a small web service that represents the protected resource. Flask is a lightweight
Python web framework we used to build it. When someone connects, it checks their IP against the
on-chain blocklist and allows or denies them."

**Q. How fast is it?**
"In our tests: detection under 50 ms, blocking under 200 ms, total attack-to-enforcement under 500
milliseconds — under half a second, fully automated."

**Q. How do you prove the record is immutable?**
"After blocking, we query the contract again with `getBlockedIPs` and the IP is still there. Since
it lives on the blockchain, it can't be silently edited or deleted — that's a verifiable audit
trail."

---

## The limitations / future-work questions

**Q. What are the limitations of your project?** ⭐
"It runs on a single node with a single signing key, so the blocking authority isn't decentralized
yet. Detection currently targets port scans only. And it's tested in a lab, not at production
scale. These are exactly the things in our future work."

**Q. How would you improve it?**
"Deploy on a public or consortium blockchain for multi-party trust; add machine-learning detection
for more attack types; enforce at the network level with iptables/firewalls; build a dashboard;
add multi-node, multi-signature authorisation; and test at scale."

**Q. Why is this better than a normal firewall?**
"A firewall blocks, but its rule list is centralized and can be edited or deleted without trace.
We add an immutable, transparent record of every block, plus instant alerting and automatic,
code-driven enforcement."

---

## The "gotcha" questions (stay calm, give the honest answer)

**Q. So is the security itself decentralized?**
"No — and we're clear about that. Only the *record* is decentralized and immutable. The detection
and enforcement run on the defender machine. We describe it honestly as a hybrid system."

**Q. Could the attacker just change their IP to get around the block?**
"Yes — IP-based blocking can be evaded by changing IPs, which is a known limitation of
IP-level defence. Stronger identity-based blocking is part of our future work. The value here is
fast, automatic, tamper-proof response to the scanning behaviour we detect."

**Q. Who can write to your blockchain?**
"Only the holder of our signing key — the monitor. That's why it's a private/permissioned chain."

---

## Demo-day reminders

- Both machines on the same `172.16.197.x` subnet; `ping` both ways first.
- Run the full thing once in rehearsal; record a backup video of a successful run.
- Lead with the honest framing: **hybrid system, private chain, immutable record.**
- If a demo step fails live, stay calm, explain what *should* happen, and play your backup video.
