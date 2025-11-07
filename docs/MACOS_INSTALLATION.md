# macOS Installation Guide

This guide covers installing and running the NASDAQ Stock Agent on macOS (both Intel and Apple Silicon).

## Prerequisites

### 1. Python Version
- **Required**: Python 3.9 or higher
- **Recommended**: Python 3.10 or 3.11

Check your Python version:
```bash
python3 --version
```

### 2. Xcode Command Line Tools
Some packages require compilation tools. Install them:
```bash
xcode-select --install
```

### 3. Homebrew (Optional but Recommended)
Install Homebrew for easier package management:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Installation Steps

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd nasdaq-stock-agent
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Upgrade pip
```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Set Up Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

Required environment variables:
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
MONGODB_URL=mongodb://localhost:27017/
MONGODB_DATABASE=nasdaq_stock_agent
```

### Step 6: Install and Start MongoDB

#### Option A: Using Homebrew (Recommended)
```bash
# Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Verify MongoDB is running
mongosh --eval "db.version()"
```

#### Option B: Using Docker
```bash
# Pull MongoDB image
docker pull mongo:latest

# Run MongoDB container
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Verify MongoDB is running
docker ps | grep mongodb
```

### Step 7: Verify Installation
```bash
# Test imports
python -c "import fastapi, langchain, anthropic, pymongo; print('✓ All packages imported successfully')"
```

## Apple Silicon (M1/M2/M3) Specific Issues

### Issue 1: grpcio Installation
If you encounter issues with `grpcio`:

```bash
# Install without binary
pip install grpcio --no-binary :all:
```

### Issue 2: Architecture Mismatch
Ensure you're using ARM64 Python, not x86_64:

```bash
# Check Python architecture
python3 -c "import platform; print(platform.machine())"
# Should output: arm64
```

If it shows `x86_64`, you're using Rosetta. Install native ARM Python:
```bash
# Using Homebrew
brew install python@3.11

# Verify
/opt/homebrew/bin/python3.11 -c "import platform; print(platform.machine())"
```

### Issue 3: NumPy/Pandas Issues
If you encounter NumPy or Pandas errors:

```bash
# Install with specific flags
pip install numpy --no-binary numpy
pip install pandas --no-binary pandas
```

## Running the Application

### Start the Main Application
```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py
```

The application will start on `http://localhost:8000`

### Start the MCP Server (Optional)
```bash
python mcp_server.py
```

### Start the Agent Protocol Server (Optional)
```bash
python agent_protocol_server.py
```

## Verification

### Test the REST API
```bash
curl http://localhost:8000/health
```

### Test the A2A Protocol
```bash
curl http://localhost:8000/a2a/manifest
```

### Test Stock Analysis
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I buy Apple stock?"}'
```

## Common Issues and Solutions

### Issue: Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Issue: MongoDB Connection Failed
```bash
# Check if MongoDB is running
brew services list | grep mongodb

# Restart MongoDB
brew services restart mongodb-community

# Check MongoDB logs
tail -f /opt/homebrew/var/log/mongodb/mongo.log
```

### Issue: Permission Denied
```bash
# Fix permissions
chmod +x main.py mcp_server.py agent_protocol_server.py
```

### Issue: Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: SSL Certificate Errors
```bash
# Install certificates
/Applications/Python\ 3.11/Install\ Certificates.command

# Or update certifi
pip install --upgrade certifi
```

## Performance Optimization for macOS

### 1. Use Native ARM Packages (Apple Silicon)
Ensure all packages are ARM64 native for best performance.

### 2. Increase File Descriptors
```bash
# Add to ~/.zshrc or ~/.bash_profile
ulimit -n 10240
```

### 3. MongoDB Optimization
```bash
# Edit MongoDB config
nano /opt/homebrew/etc/mongod.conf

# Add:
# storage:
#   wiredTiger:
#     engineConfig:
#       cacheSizeGB: 2
```

## Development Setup

### Install Development Tools
```bash
# Install additional dev tools
pip install ipython jupyter notebook

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agent.py -v
```

### Code Formatting
```bash
# Format code
black src/

# Check linting
flake8 src/
```

## Uninstallation

### Remove Virtual Environment
```bash
deactivate
rm -rf venv/
```

### Stop and Remove MongoDB (Homebrew)
```bash
brew services stop mongodb-community
brew uninstall mongodb-community
```

### Stop and Remove MongoDB (Docker)
```bash
docker stop mongodb
docker rm mongodb
```

## Troubleshooting Resources

- **Python Issues**: https://www.python.org/downloads/macos/
- **Homebrew Issues**: https://docs.brew.sh/Troubleshooting
- **MongoDB Issues**: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/
- **Apple Silicon Issues**: https://github.com/apple/tensorflow_macos

## Getting Help

If you encounter issues:

1. Check the logs: `tail -f logs/app.log`
2. Verify environment variables: `cat .env`
3. Check MongoDB connection: `mongosh`
4. Review system requirements: `python --version`, `pip list`

For additional support, please open an issue on GitHub with:
- macOS version: `sw_vers`
- Python version: `python3 --version`
- Architecture: `uname -m`
- Error messages and logs