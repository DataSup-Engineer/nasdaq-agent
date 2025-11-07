# Quick Start Guide

## ✅ All Bugs Fixed!

1. ✅ `AttributeError: 'CompanyNameResolver' object has no attribute 'common_words'` - FIXED
2. ✅ `ValidationError: Extra inputs are not permitted (mcp_enabled, mcp_host, mcp_port)` - FIXED
3. ✅ `RuntimeError: no running event loop` in LoggingService - FIXED
4. ✅ `ModuleNotFoundError: No module named 'fastapi.middleware.base'` - FIXED

## Prerequisites

1. **Python 3.9+** installed
2. **MongoDB** installed and running
3. **Anthropic API Key** (get from https://console.anthropic.com/)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Anthropic API key
nano .env
```

**Required:** Replace `your_anthropic_api_key_here` with your actual API key:
```
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

### 3. Start MongoDB

```bash
# macOS (Homebrew)
brew services start mongodb-community

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 4. Run the Application

```bash
python main.py
```

**Expected Output:**
```
INFO - Starting NASDAQ Stock Agent v1.0.0
INFO - Database initialized successfully
INFO - MCP server initialized successfully
INFO - A2A handler initialized successfully
INFO - All services initialized successfully
INFO - Starting server on 0.0.0.0:8000
```

### 5. Test the Application

```bash
# Health check
curl http://localhost:8000/health

# Test stock analysis
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I buy Apple stock?"}'

# Test A2A protocol
curl http://localhost:8000/a2a/manifest
```

## Common Issues

### Issue: AttributeError about 'common_words'
**Status:** ✅ FIXED
**Solution:** Already fixed in the code

### Issue: "Anthropic API key not configured"
**Solution:** 
1. Create `.env` file from `.env.example`
2. Add your Anthropic API key
3. Restart the application

### Issue: "MongoDB connection failed"
**Solution:**
```bash
# Check if MongoDB is running
brew services list | grep mongodb

# Start MongoDB
brew services start mongodb-community

# Or check Docker
docker ps | grep mongodb
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in .env
PORT=8001
```

## Verification

After starting the application, verify everything works:

```bash
# 1. Check health
curl http://localhost:8000/health

# Expected: {"status":"healthy",...}

# 2. Check system status
curl http://localhost:8000/status

# 3. Check A2A manifest
curl http://localhost:8000/a2a/manifest

# 4. Check MCP status
curl http://localhost:8000/health/mcp
```

## Next Steps

1. **Read the API Documentation**: Visit http://localhost:8000/docs
2. **Test Stock Analysis**: Try analyzing different stocks
3. **Explore A2A Protocol**: See `docs/A2A_PROTOCOL.md`
4. **Check MCP Integration**: See MCP server documentation

## Getting Help

- **Installation Issues**: See `docs/MACOS_INSTALLATION.md`
- **Dependency Conflicts**: See `docs/A2A_PACKAGE_CONFLICT.md`
- **API Documentation**: http://localhost:8000/docs
- **System Requirements**: See `docs/REQUIREMENTS_VERIFICATION.md`

## Summary

✅ Dependencies installed  
✅ Bug fixed  
✅ Environment configured  
✅ MongoDB running  
✅ Application started  
✅ Ready to analyze stocks!

Enjoy using the NASDAQ Stock Agent! 🚀