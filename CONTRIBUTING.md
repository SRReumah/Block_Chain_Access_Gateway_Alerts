# Contributing to Blockchain Access Gateway

Thank you for your interest in contributing! This guide explains how to collaborate on this project smoothly.

---

## 🎯 Code of Conduct

- Be respectful and constructive in all interactions
- Provide helpful feedback on PRs
- Focus on code, not people, in reviews

---

## 🔄 Git Workflow

### 1. Fork & Clone
```bash
# Fork on GitHub, then clone YOUR fork
git clone https://github.com/YOUR_USERNAME/Block_Chain_Access_Gateway_Alerts.git
cd Block_Chain_Access_Gateway_Alerts

# Add upstream remote
git remote add upstream https://github.com/SRReumah/Block_Chain_Access_Gateway_Alerts.git
```

### 2. Create a Feature Branch
Always create a new branch for your work. Never commit to `main`.

```bash
# Update main first
git fetch upstream
git checkout main
git merge upstream/main

# Create your feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/add-dashboard` – New functionality
- `fix/telegram-timeout` – Bug fix
- `docs/update-readme` – Documentation
- `test/add-unit-tests` – Tests
- `refactor/clean-monitor` – Code improvements

### 3. Make Changes & Commit

```bash
# Edit files in VS Code
git add .
git commit -m "Clear, descriptive message"
```

**Good commit messages:**
- ✅ `Add Telegram integration for alerts`
- ✅ `Fix contract deployment script timeout`
- ✅ `Update README with quick start guide`
- ❌ `fixed stuff`
- ❌ `Update`

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

Go to your fork on GitHub and click **"Compare & Pull Request"**

In your PR description, include:
- What you changed and why
- If it fixes an issue, reference it: `Fixes #123`
- Any testing you did
- Known limitations (if any)

**Example PR description:**
```
## Description
Added a web dashboard for viewing blocked IPs in real-time.

## Changes
- Created `dashboard.py` with Flask routes
- Added HTML template for IP blocklist view
- Updated `requirements.txt` with new dependencies

## Testing
- Tested locally with 10 blocked IPs
- Verified refresh rate is <1 second
- No performance impact on monitor.py

## Fixes
Addresses #15 (Dashboard feature request)
```

### 6. Address Review Feedback

- Sherin (or another reviewer) will review your PR
- They may request changes
- Make edits on your local branch and push again:
  ```bash
  git add .
  git commit -m "Address PR feedback: update validation"
  git push origin feature/your-feature-name
  ```
- The PR updates automatically

### 7. After Merge

Once your PR is merged:
```bash
# Switch back to main
git checkout main

# Get the latest code
git fetch upstream
git merge upstream/main

# Optional: delete your local feature branch
git branch -d feature/your-feature-name
```

---

## 📝 What to Contribute

### High Priority
- **Documentation** – README, setup guides, usage examples
- **Bug fixes** – Found a bug? Open an issue first, then PR
- **Tests** – Unit and integration tests
- **Dashboard/UI** – Web interface for viewing blocklists
- **ML detection** – Anomaly detection beyond nmap scans

### Great for Beginners
- Improve README or other docs
- Add comments to code
- Update `.env.example`
- Fix typos or grammar

---

## 🧪 Testing Before You Submit

### Unit Tests
```bash
npx hardhat test
```

### Manual Testing
```bash
# Terminal 1: Start Hardhat
npx hardhat node

# Terminal 2: Deploy contract
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3: Run monitor
sudo python3 monitor.py

# Terminal 4: Run gateway
python3 gateway.py

# Terminal 5: Test from attacker
nmap -sS 172.16.32.119
```

---

## 📋 Code Style Guide

### Python
```python
# Use clear variable names
blocked_ips = []  # Good
bips = []         # Bad

# Use docstrings
def check_if_blocked(ip_address):
    """Check if an IP is in the blockchain blocklist."""
    return ip_address in blocklist

# Comments explain WHY, not WHAT
# Good: Wait for contract to confirm on-chain before enforcing
time.sleep(2)

# Bad: Sleep
time.sleep(2)
```

### Solidity
```solidity
// Use OpenZeppelin patterns
pragma solidity ^0.8.0;

// Clear naming
mapping(address => bool) public blockedAddresses;  // Good
mapping(address => bool) public b;                  // Bad
```

### JavaScript
```javascript
// Use const by default
const blocklistContract = new ethers.Contract(address, ABI, signer);

// Use async/await
async function deployContract() {
  const Blocklist = await ethers.getContractFactory("Blocklist");
  const contract = await Blocklist.deploy();
  return contract;
}
```

---

## 📖 Documentation Standards

When adding features, also add docs:

1. **Code comments** – Explain complex logic
2. **Docstrings** – Function/class descriptions
3. **README updates** – If it's a major feature
4. **USAGE.md updates** – How to use the feature
5. **ARCHITECTURE.md** – If it changes system design

**Example:**
```python
def block_ip_on_chain(ip_address: str) -> str:
    """
    Block an IP address by recording it on the blockchain.
    
    Args:
        ip_address (str): The IP to block (e.g., "172.16.32.209")
    
    Returns:
        str: Transaction hash of the blockchain recording
    
    Raises:
        ValueError: If IP format is invalid
        Exception: If contract interaction fails
    
    Example:
        >>> tx_hash = block_ip_on_chain("172.16.32.209")
        >>> print(f"Blocked: {tx_hash}")
    """
```

---

## 🐛 Reporting Bugs

Found a bug? Open a GitHub Issue:

1. Go to [Issues](../../issues)
2. Click **"New Issue"**
3. Provide:
   - **Title** – Clear, short description
   - **Environment** – OS, Python version, Node version
   - **Steps to reproduce** – Exact commands/actions
   - **Expected behavior** – What should happen
   - **Actual behavior** – What happened instead
   - **Logs** – Error messages, stack traces

**Example:**
```
Title: Monitor crashes when Hardhat node restarts

Environment:
- Kali Linux 2023.4
- Python 3.10
- Node 18.12.0

Steps to reproduce:
1. Start monitor.py
2. Start Hardhat node
3. Stop Hardhat node (Ctrl+C)
4. Restart Hardhat node

Expected: Monitor reconnects gracefully
Actual: Monitor crashes with ConnectionError

Logs:
Traceback (most recent call last):
  File "monitor.py", line 45, in connect
    ...
ConnectionError: Failed to connect to contract
```

---

## 🎓 Useful Resources

- [GitHub Fork Guide](https://docs.github.com/en/get-started/quickstart/fork-a-repo)
- [Creating a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
- [Solidity Best Practices](https://solidity.readthedocs.io/en/v0.8.0/)
- [Web3.py Documentation](https://web3py.readthedocs.io/)

---

## ✅ Checklist Before Submitting PR

- [ ] I created a new branch (not working on `main`)
- [ ] My code follows the style guide above
- [ ] I tested my changes locally
- [ ] I added/updated documentation
- [ ] I added comments for complex code
- [ ] My commit messages are clear
- [ ] I linked any related issues
- [ ] No merge conflicts with upstream/main

---

## 🙏 Thank You!

Your contributions make this project better. We appreciate your time and effort!

---

**Questions?** Open a GitHub Discussion or reach out to the maintainers.
