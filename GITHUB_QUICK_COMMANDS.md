# GitHub Quick Commands - Copy & Paste

## 🚀 Push to GitHub in 5 Steps

### Step 1: Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 2: Initialize and Add Files
```bash
cd "/Users/suprajmudda/Documents/CapStone Project/AI Agent-Project"
git init
git add .
```

### Step 3: Create Initial Commit
```bash
git commit -m "Initial commit: NASDAQ Stock Agent with MCP and A2A protocols"
```

### Step 4: Connect to GitHub
**First, create a repository on GitHub.com, then:**
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git
git branch -M main
```

### Step 5: Push to GitHub
```bash
git push -u origin main
```

---

## ✅ Safety Check

Before pushing, verify:
```bash
git status
```

**Should NOT see** (protected by .gitignore):
- ❌ `.env` (your API keys are SAFE!)
- ❌ `venv/` (not needed on GitHub)
- ❌ `__pycache__/` (not needed)

**Should see**:
- ✅ `src/` (your code)
- ✅ `requirements.txt`
- ✅ `main.py`
- ✅ `.env.example` (template only, no secrets)

---

## 🔑 GitHub Authentication

When prompted for password, use a **Personal Access Token**:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "NASDAQ Stock Agent"
4. Select: `repo` (full control)
5. Generate and **COPY THE TOKEN**
6. Paste token when prompted for password

---

## 📝 Update Repository Later

```bash
# After making changes
git add .
git commit -m "Description of your changes"
git push
```

---

## 🆘 Common Issues

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git
```

### "Updates were rejected"
```bash
git pull origin main --rebase
git push origin main
```

### Accidentally committed .env
```bash
git rm --cached .env
git commit -m "Remove .env"
git push
# Then regenerate your API keys!
```

---

## 📚 Full Guide

See `GITHUB_DEPLOYMENT.md` for complete documentation.

---

## ✨ That's It!

Your code is now on GitHub! 🎉

Repository URL: `https://github.com/YOUR_USERNAME/nasdaq-stock-agent`