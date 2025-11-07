# A2A Package Dependency Conflict Resolution

## Issue

The official `agent-protocol` package has a dependency conflict with newer versions of FastAPI:

- **agent-protocol 1.0.x** requires `fastapi<0.101.0`
- **Our application** uses `fastapi>=0.104.0` for latest features

This creates a dependency conflict that pip cannot resolve.

## Solution: Use Custom A2A Implementation

**Install with:**
```bash
pip install -r requirements.txt
```

**Features:**
- ✅ Uses FastAPI 0.104+ (latest features)
- ✅ Custom A2A protocol implementation
- ✅ All A2A endpoints work perfectly
- ✅ No dependency conflicts
- ✅ No external agent-protocol package needed

**A2A Endpoints Available:**
- `GET /a2a/manifest` - Agent manifest
- `GET /a2a/capabilities` - List capabilities
- `POST /a2a/request` - Full A2A request
- `POST /a2a/capabilities/{id}/invoke` - Invoke capability
- `GET /a2a/agent` - Agent info (custom format)
- `POST /a2a/tasks` - Task execution (custom format)

### Alternative: Manual Installation of agent-protocol

If you specifically need the official agent-protocol package, you can install it manually:

```bash
# This will downgrade FastAPI to 0.100.x
pip install agent-protocol==1.0.2
```

**Note:** This is not recommended as it creates dependency conflicts and downgrades FastAPI.

## Why Custom A2A is the Solution

| Feature | Custom A2A (Included) |
|---------|----------------------|
| FastAPI Version | ✅ 0.104+ (latest) |
| A2A Protocol | ✅ Full implementation |
| Dependency Conflicts | ✅ None |
| Agent Discovery | ✅ Yes |
| Task Execution | ✅ Yes |
| MCP Support | ✅ Yes |
| REST API | ✅ Yes |
| Installation | ✅ Simple |

## Recommendation

**Use the standard installation** with `requirements.txt`. The custom A2A implementation provides all the functionality you need without dependency conflicts.

### Why Custom A2A is Better

1. **No Conflicts**: Uses latest FastAPI without issues
2. **Same Functionality**: All A2A features work identically
3. **Better Performance**: Latest FastAPI optimizations
4. **More Features**: Access to FastAPI 0.104+ features
5. **Easier Maintenance**: No version pinning issues

### When to Use Official agent-protocol

- You need strict agent-protocol standard compliance
- You're integrating with tools that require the official package
- You're okay with using FastAPI 0.100.x

## Current Installation Status

Based on your error, you're currently trying to install both:
- `fastapi>=0.104.0` (from requirements.txt)
- `agent-protocol>=1.0.0` (which requires fastapi<0.101.0)

This creates the conflict.

## How to Fix Your Installation

### Quick Fix (Recommended)

```bash
# Remove agent-protocol from requirements.txt (already done)
pip install -r requirements.txt
```

The updated requirements.txt no longer includes agent-protocol, so the conflict is resolved.

### If You Absolutely Need agent-protocol

```bash
# Install manually (not recommended - causes conflicts)
pip install agent-protocol==1.0.2
```

**Warning:** This will downgrade FastAPI to 0.100.x and may cause issues.

## Testing Your Installation

After installing, verify everything works:

```bash
# Test imports
python3 -c "
import fastapi
import langchain
import anthropic
from src.a2a.agent_protocol_adapter import AGENT_PROTOCOL_AVAILABLE
print(f'FastAPI version: {fastapi.__version__}')
print(f'agent-protocol available: {AGENT_PROTOCOL_AVAILABLE}')
print('✅ Installation successful!')
"

# Start the application
python main.py

# Test A2A endpoints
curl http://localhost:8000/a2a/manifest
curl http://localhost:8000/a2a/capabilities
```

## A2A Implementation Details

### Custom A2A (Option 1)

Our custom implementation provides:

**Message Format:**
```json
{
  "message_id": "uuid",
  "message_type": "request",
  "capability_id": "nasdaq.analyze_stock",
  "parameters": {"company_name_or_ticker": "Apple"}
}
```

**Response Format:**
```json
{
  "message_id": "uuid",
  "success": true,
  "result": {...},
  "processing_time_ms": 1234
}
```

### Official agent-protocol (Option 2)

Uses standard agent-protocol format:

**Task Format:**
```json
{
  "action": "analyze_stock",
  "parameters": {"company_name_or_ticker": "Apple"}
}
```

**Response Format:**
```json
{
  "task_id": "task_123",
  "status": "completed",
  "result": {...}
}
```

## If You Accidentally Installed agent-protocol

```bash
# Remove agent-protocol and reinstall
pip uninstall -y agent-protocol fastapi uvicorn
pip install -r requirements.txt
```

This will restore FastAPI to 0.104+ and remove the conflict.

## Future Resolution

The dependency conflict will be resolved when:
1. agent-protocol updates to support FastAPI 0.104+
2. We can use both packages together

Until then, choose the option that best fits your needs.

## Support

- **Custom A2A Issues**: See `docs/A2A_PROTOCOL.md`
- **agent-protocol Issues**: See `docs/A2A_IMPLEMENTATION.md`
- **Installation Issues**: See `docs/MACOS_INSTALLATION.md`

## Summary

✅ **Recommended**: Use `requirements.txt` (custom A2A, no conflicts)  
⚠️ **Alternative**: Use `requirements-agent-protocol.txt` (official package, downgrades FastAPI)

Both options provide full A2A functionality. The custom implementation is recommended for most users.