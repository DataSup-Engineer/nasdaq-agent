# GitHub Deployment Guide

## 🚀 Complete Guide to Push Your Code to GitHub

### Prerequisites

- Git installed on your Mac
- GitHub account created
- Repository created on GitHub (or will create one)

---

## Step 1: Verify Git Installation

```bash
# Check if git is installed
git --version

# If not installed, install via Homebrew
brew install git
```

---

## Step 2: Configure Git (First Time Only)

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Verify configuration
git config --list
```

---

## Step 3: Initialize Git Repository (If Not Already Done)

```bash
# Navigate to your project directory
cd "/Users/suprajmudda/Documents/CapStone Project/AI Agent-Project"

# Initialize git repository
git init

# Check status
git status
```

---

## Step 4: Review What Will Be Committed

```bash
# See what files will be added
git status

# The .gitignore file will prevent these from being uploaded:
# - .env (your API keys - SAFE!)
# - venv/ (virtual environment - not needed)
# - __pycache__/ (Python cache - not needed)
# - *.log (log files - not needed)
```

---

## Step 5: Add Files to Git

```bash
# Add all files (respecting .gitignore)
git add .

# Or add specific files/folders
git add src/
git add requirements.txt
git add main.py
git add README.md
git add docs/

# Check what's staged
git status
```

---

## Step 6: Create Initial Commit

```bash
# Commit with a descriptive message
git commit -m "Initial commit: NASDAQ Stock Agent with MCP and A2A protocols

- Implemented REST API with FastAPI
- Added MCP (Model Context Protocol) server integration
- Added A2A (Agent-to-Agent) protocol support
- Integrated Langchain with Anthropic Claude
- MongoDB logging and caching
- Fixed all startup bugs
- Complete documentation"

# Verify commit
git log --oneline
```

---

## Step 7: Create GitHub Repository

### Option A: Via GitHub Website

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Repository name: `nasdaq-stock-agent` (or your choice)
4. Description: "AI-powered NASDAQ stock analysis agent with MCP and A2A protocols"
5. Choose: **Public** or **Private**
6. **DO NOT** initialize with README (you already have one)
7. Click "Create repository"

### Option B: Via GitHub CLI (if installed)

```bash
# Install GitHub CLI
brew install gh

# Login to GitHub
gh auth login

# Create repository
gh repo create nasdaq-stock-agent --public --source=. --remote=origin
```

---

## Step 8: Connect to GitHub Repository

```bash
# Add GitHub as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git

# Verify remote
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git (fetch)
# origin  https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git (push)
```

---

## Step 9: Push to GitHub

```bash
# Push to main branch
git push -u origin main

# If you get an error about 'master' vs 'main', rename branch:
git branch -M main
git push -u origin main
```

### If Authentication Required

You'll need a Personal Access Token (PAT):

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "NASDAQ Stock Agent"
4. Select scopes: `repo` (full control)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. When prompted for password, paste the token

---

## Step 10: Verify Upload

```bash
# Check remote repository
git remote show origin

# Visit your repository
# https://github.com/YOUR_USERNAME/nasdaq-stock-agent
```

---

## Step 11: Create a Great README (Optional but Recommended)

Create a `README.md` in the root if you don't have one:

```bash
# Create README
cat > README.md << 'EOF'
# NASDAQ Stock Agent

AI-powered NASDAQ stock analysis and investment recommendations using Langchain, Anthropic Claude, and real-time market data.

## Features

- 🤖 AI-powered stock analysis with Anthropic Claude
- 📊 Real-time market data from Yahoo Finance
- 🔌 MCP (Model Context Protocol) server integration
- 🤝 A2A (Agent-to-Agent) protocol support
- 📝 Complete audit trail with MongoDB
- 🚀 FastAPI REST API
- 🧠 Langchain agent orchestration

## Quick Start

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your Anthropic API key to .env

# Start MongoDB
brew services start mongodb-community

# Run the application
python main.py
\`\`\`

## Documentation

- [Quick Start Guide](QUICKSTART.md)
- [macOS Installation](docs/MACOS_INSTALLATION.md)
- [All Bugs Fixed](ALL_BUGS_FIXED.md)
- [A2A Protocol](docs/A2A_PROTOCOL.md)
- [Agent Protocols](docs/AGENT_PROTOCOLS.md)

## Requirements

- Python 3.9+
- MongoDB
- Anthropic API Key

## License

MIT License
EOF

# Add and commit README
git add README.md
git commit -m "Add comprehensive README"
git push
```

---

## Complete Command Sequence (Copy & Paste)

```bash
# Navigate to project
cd "/Users/suprajmudda/Documents/CapStone Project/AI Agent-Project"

# Initialize git (if not done)
git init

# Configure git (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: NASDAQ Stock Agent with MCP and A2A protocols"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Safety Checklist

Before pushing, verify these files are **NOT** included:

```bash
# Check what will be pushed
git status

# These should NOT appear (protected by .gitignore):
# ❌ .env (contains API keys)
# ❌ venv/ (virtual environment)
# ❌ __pycache__/ (Python cache)
# ❌ *.log (log files)
# ❌ .DS_Store (Mac system files)

# These SHOULD be included:
# ✅ src/ (source code)
# ✅ requirements.txt
# ✅ main.py
# ✅ .env.example (template, no secrets)
# ✅ docs/
# ✅ README.md
# ✅ .gitignore
```

---

## Updating Your Repository Later

```bash
# After making changes
git add .
git commit -m "Description of changes"
git push

# Or specific files
git add src/api/app.py
git commit -m "Update API endpoints"
git push
```

---

## Common Issues and Solutions

### Issue: "fatal: remote origin already exists"

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/nasdaq-stock-agent.git
```

### Issue: "Updates were rejected"

```bash
# Pull first, then push
git pull origin main --rebase
git push origin main
```

### Issue: "Authentication failed"

```bash
# Use Personal Access Token instead of password
# Generate at: https://github.com/settings/tokens
```

### Issue: ".env file was accidentally committed"

```bash
# Remove from git but keep locally
git rm --cached .env
git commit -m "Remove .env from repository"
git push

# Then regenerate your API keys for security!
```

---

## Best Practices

1. **Never commit secrets**: Always use `.env.example` as template
2. **Commit often**: Small, focused commits are better
3. **Write good commit messages**: Describe what and why
4. **Use branches**: For new features, create branches
5. **Review before pushing**: Always check `git status` first

---

## Creating Branches (Advanced)

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Make changes, commit
git add .
git commit -m "Add new feature"

# Push branch
git push -u origin feature/new-feature

# Switch back to main
git checkout main

# Merge branch
git merge feature/new-feature
```

---

## Repository Structure on GitHub

```
nasdaq-stock-agent/
├── .github/              # GitHub workflows (optional)
├── .kiro/               # Kiro configuration
├── docs/                # Documentation
├── src/                 # Source code
│   ├── a2a/            # A2A protocol
│   ├── agents/         # Langchain agents
│   ├── api/            # FastAPI routes
│   ├── config/         # Configuration
│   ├── core/           # Core dependencies
│   ├── mcp/            # MCP server
│   ├── models/         # Data models
│   └── services/       # Business logic
├── scripts/            # Utility scripts
├── .env.example        # Environment template
├── .gitignore          # Git ignore rules
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── QUICKSTART.md       # Quick start guide
└── ALL_BUGS_FIXED.md   # Bug fixes documentation
```

---

## Success!

Once pushed, your repository will be available at:
```
https://github.com/YOUR_USERNAME/nasdaq-stock-agent
```

You can now:
- Share the link with others
- Clone it on other machines
- Collaborate with team members
- Track issues and pull requests
- Set up CI/CD pipelines

---

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Docs: https://git-scm.com/doc
- GitHub CLI: https://cli.github.com

Happy coding! 🚀