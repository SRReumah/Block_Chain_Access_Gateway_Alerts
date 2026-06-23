# Git Quick Reference

Copy-paste commands for your GitHub workflow. Print this or bookmark it!

---

## 🔧 Initial Setup (One-time)

```bash
# Fork on GitHub, then clone YOUR fork
git clone https://github.com/YOUR_USERNAME/Block_Chain_Access_Gateway_Alerts.git
cd Block_Chain_Access_Gateway_Alerts

# Add upstream remote (Sherin's repo)
git remote add upstream https://github.com/SRReumah/Block_Chain_Access_Gateway_Alerts.git

# Verify remotes
git remote -v
```

---

## 📝 Before Starting Work

```bash
# Fetch latest from Sherin's repo
git fetch upstream

# Switch to main branch
git checkout main

# Merge the latest changes
git merge upstream/main

# Verify you're up-to-date
git log --oneline -5
```

---

## 🚀 Create & Work on Feature Branch

```bash
# Create a new branch for your feature
git checkout -b feature/your-feature-name

# Edit files in VS Code, then save

# Check what you changed
git status

# Stage your changes
git add .

# Or stage specific files
git add monitor.py contracts/Blocklist.sol

# Commit with a clear message
git commit -m "Add feature description here"

# Verify commit
git log --oneline -3
```

---

## 📤 Push to Your Fork & Create PR

```bash
# Push your branch to YOUR fork on GitHub
git push origin feature/your-feature-name

# Then go to GitHub and click "Compare & Pull Request"
```

---

## 🔄 After Review & Merge

```bash
# Switch back to main
git checkout main

# Get latest from both upstream and your fork
git fetch upstream
git fetch origin

# Merge Sherin's changes
git merge upstream/main

# Delete your local feature branch (optional)
git branch -d feature/your-feature-name
```

---

## 🐛 Common Fixes

### Undo last commit (before pushing)
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Discard changes too
git reset --hard HEAD~1
```

### Accidentally committed to main?
```bash
# Create a branch from main
git checkout -b feature/my-feature

# Go back to main and reset
git checkout main
git reset --hard origin/main
```

### Forgot to add something to commit?
```bash
# Add missing files
git add missing-file.py

# Amend commit (before pushing!)
git commit --amend --no-edit
```

### Merge conflict?
```bash
# Pull latest and resolve conflicts
git pull upstream main

# Fix conflicts in VS Code, then:
git add .
git commit -m "Resolve merge conflicts"
git push origin feature/your-feature
```

---

## 👀 View Status & Logs

```bash
# See your current branch
git branch

# See all branches (local + remote)
git branch -a

# See uncommitted changes
git status

# See changes in a file
git diff file.py

# See commit history
git log --oneline -10

# See who changed a line
git blame file.py
```

---

## 📊 Check Before Pushing

```bash
# See commits not yet pushed
git log origin/feature/your-feature..HEAD

# See what will be pushed
git diff --stat origin/feature/your-feature...HEAD

# Verify branch is up-to-date
git fetch origin
git log --oneline origin/feature/your-feature..HEAD
```

---

## 🔗 VS Code Git Integration

All commands above can also be done in VS Code:

1. **Source Control tab** (Ctrl+Shift+G)
2. **Command Palette** (Ctrl+Shift+P) → type "Git: "
3. **Terminal** (Ctrl+`) → type git commands directly

### In VS Code:
- **Stage files:** Click `+` icon
- **Commit:** Write message, click checkmark
- **Push:** Click `...` menu → Push
- **Pull:** Click `...` menu → Pull
- **Create branch:** Click branch name → Create Branch

---

## 🚨 Emergency Commands

### See everything I changed
```bash
git diff origin/main...HEAD
```

### Abort merge/rebase
```bash
git merge --abort
git rebase --abort
```

### Go back to last working state
```bash
git reset --hard origin/main
```

### See all my unpushed commits
```bash
git log origin/main..HEAD
```

---

## 💡 Pro Tips

### Make your branch track upstream
```bash
git push -u origin feature/your-feature
# Now just use `git push` and `git pull` without arguments
```

### Clean up old branches
```bash
# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature
```

### Squash commits before PR (optional)
```bash
# Combine last 3 commits into 1
git rebase -i HEAD~3
# In editor: keep first as 'pick', change others to 'squash'
# Force push (only on your feature branch!)
git push origin feature/your-feature --force
```

### Create alias for common commands
```bash
# In terminal, add to ~/.bashrc or ~/.zshrc:
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

# Then use: git co feature/test, git br, git ci -m "msg", etc.
```

---

## 📚 Full Workflow in 30 Seconds

```bash
# 1. Prep (before any work)
git fetch upstream
git checkout main
git merge upstream/main

# 2. Work (create branch, make changes)
git checkout -b feature/awesome-feature
# [edit files in VS Code]

# 3. Commit (stage and commit)
git add .
git commit -m "Add awesome feature"

# 4. Push (send to GitHub)
git push origin feature/awesome-feature

# 5. PR (go to GitHub, click "Compare & Pull Request")
# [Wait for Sherin to review & merge]

# 6. Sync (get latest)
git fetch upstream
git checkout main
git merge upstream/main
```

---

## ❓ Quick Help

```bash
# Get help for any command
git help commit
git help merge
git help rebase

# Or search online:
# "git [command] tutorial"
```

---

**Save this file and reference it whenever you're unsure!**

For detailed explanations, see [CONTRIBUTING.md](./CONTRIBUTING.md)
