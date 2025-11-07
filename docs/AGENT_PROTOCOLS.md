# Agent Communication Protocols

The NASDAQ Stock Agent supports multiple protocols for agent-to-agent communication and integration.

## Supported Protocols

### 1. MCP (Model Context Protocol)

**Purpose**: Standardized tool interface for AI agent frameworks

**Transport**: stdio (standard input/output)

**Use Case**: Integration with AI development frameworks like Claude Desktop, LangChain, etc.

**Key Features**:
- Tool-based interface
- Standardized tool schemas
- Request/response pattern
- Designed for AI agent frameworks

**Documentation**: See MCP server implementation in `src/mcp/`

**Endpoints**:
- Health check: `GET /health/mcp`
- Status: Available through health endpoints

**Tools Available**:
- `analyze_stock`: Comprehensive stock analysis
- `get_market_data`: Market data retrieval
- `resolve_company_name`: Company name resolution

**Running MCP Server**:
```bash
python mcp_server.py
```

---

### 2. A2A (Agent-to-Agent Protocol)

**Purpose**: Direct agent-to-agent communication via REST API

**Transport**: HTTP/REST

**Package**: Uses official `agent-protocol` Python package (optional but recommended)

**Use Case**: Direct integration between autonomous agents, multi-agent systems

**Key Features**:
- Agent discovery via manifest
- Capability-based invocation
- Structured messaging format
- Conversation tracking
- Full audit trail
- Compatible with agent-protocol standard

**Documentation**: See `docs/A2A_PROTOCOL.md`

**Installation**:
```bash
pip install agent-protocol
```

**Endpoints**:
- Agent Info: `GET /a2a/agent` (agent-protocol standard)
- Create Task: `POST /a2a/tasks` (agent-protocol standard)
- Manifest: `GET /a2a/manifest` (custom A2A)
- Capabilities: `GET /a2a/capabilities` (custom A2A)
- Request: `POST /a2a/request` (custom A2A)
- Invoke: `POST /a2a/capabilities/{id}/invoke` (custom A2A)
- Status: `GET /a2a/status`
- Health: `GET /a2a/health`

**Capabilities Available**:
- `nasdaq.analyze_stock`: AI-powered stock analysis
- `nasdaq.get_market_data`: Market data retrieval
- `nasdaq.resolve_company_name`: Company name to ticker resolution
- `nasdaq.query`: Natural language query processing

**Example Usage**:
```python
# Using official agent-protocol package
from agent_protocol import Agent

agent = Agent(base_url="http://localhost:8001")
task = await agent.create_task({
    "action": "analyze_stock",
    "parameters": {"company_name_or_ticker": "Apple"}
})

# Or using REST API directly
import requests

# Get agent info (agent-protocol standard)
agent_info = requests.get("http://localhost:8000/a2a/agent").json()

# Create task (agent-protocol standard)
task = requests.post(
    "http://localhost:8000/a2a/tasks",
    json={"action": "analyze_stock", "parameters": {"company_name_or_ticker": "Apple"}}
).json()

# Or use custom A2A endpoints
manifest = requests.get("http://localhost:8000/a2a/manifest").json()
response = requests.post(
    "http://localhost:8000/a2a/capabilities/nasdaq.analyze_stock/invoke",
    json={"company_name_or_ticker": "Apple"}
)
```

---

### 3. REST API

**Purpose**: Traditional HTTP API for web applications and services

**Transport**: HTTP/REST

**Use Case**: Web applications, mobile apps, traditional integrations

**Key Features**:
- OpenAPI/Swagger documentation
- JSON request/response
- Standard HTTP methods
- Rate limiting and authentication ready

**Documentation**: Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

**Main Endpoints**:
- Analyze: `POST /api/v1/analyze`
- Agent Info: `GET /api/v1/agent/info`
- Health: `GET /health`
- Status: `GET /status`

---

## Protocol Comparison

| Feature | MCP | A2A | REST API |
|---------|-----|-----|----------|
| **Transport** | stdio | HTTP | HTTP |
| **Message Format** | MCP Protocol | A2A Messages | JSON |
| **Discovery** | Tool List | Agent Manifest | OpenAPI Spec |
| **Use Case** | AI Frameworks | Agent-to-Agent | Web Apps |
| **Conversation Tracking** | No | Yes | No |
| **Audit Trail** | Yes | Yes | Yes |
| **Authentication** | N/A | Ready | Ready |

## Choosing a Protocol

### Use MCP when:
- Integrating with AI development frameworks
- Building tool-based AI agents
- Using Claude Desktop or similar platforms
- Need stdio-based communication

### Use A2A when:
- Building multi-agent systems
- Need agent discovery and capability negotiation
- Want conversation tracking across requests
- Building autonomous agent networks
- Need structured agent-to-agent messaging

### Use REST API when:
- Building web applications
- Need traditional HTTP integration
- Want OpenAPI/Swagger documentation
- Building mobile apps or services

## Common Features

All protocols share:

1. **Same Underlying Services**: All protocols use the same Langchain agent and services
2. **Unified Logging**: All requests logged to MongoDB with 30-day retention
3. **Same Capabilities**: Access to stock analysis, market data, and company resolution
4. **Error Handling**: Consistent error handling and reporting
5. **Performance Monitoring**: All requests tracked in performance metrics

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   External Clients                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ AI Agent │  │  Agent   │  │   Web Application    │  │
│  │Framework │  │  System  │  │   Mobile App         │  │
│  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘  │
└───────┼─────────────┼───────────────────┼──────────────┘
        │             │                   │
        │ MCP         │ A2A               │ REST
        │ (stdio)     │ (HTTP)            │ (HTTP)
        │             │                   │
┌───────▼─────────────▼───────────────────▼──────────────┐
│              NASDAQ Stock Agent                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │   MCP    │  │   A2A    │  │      REST API        │  │
│  │  Server  │  │ Handler  │  │      Routers         │  │
│  └────┬─────┘  └────┬─────┘  └──────────┬───────────┘  │
│       └─────────────┴───────────────────┘              │
│                      │                                  │
│         ┌────────────▼────────────┐                     │
│         │  Langchain Agent        │                     │
│         │  Stock Analysis         │                     │
│         └────────────┬────────────┘                     │
│                      │                                  │
│    ┌─────────────────┼─────────────────┐               │
│    │                 │                 │               │
│ ┌──▼───┐  ┌─────────▼────────┐  ┌────▼─────┐          │
│ │Market│  │Investment Analysis│  │   NLP    │          │
│ │ Data │  │     Service       │  │ Service  │          │
│ └──────┘  └──────────────────┘  └──────────┘          │
│                                                         │
│         ┌────────────────────────────┐                 │
│         │   MongoDB (Logging)        │                 │
│         │   30-day retention         │                 │
│         └────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

## Getting Started

### 1. Start the Main Application
```bash
python main.py
```

This starts:
- REST API on port 8000
- A2A protocol endpoints
- MCP server (if enabled in config)

### 2. Access Different Protocols

**REST API**:
```bash
curl http://localhost:8000/docs
```

**A2A Protocol**:
```bash
curl http://localhost:8000/a2a/manifest
```

**MCP Server** (separate process):
```bash
python mcp_server.py
```

### 3. Test the Protocols

**REST API**:
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I buy Apple stock?"}'
```

**A2A Protocol**:
```bash
curl -X POST http://localhost:8000/a2a/capabilities/nasdaq.analyze_stock/invoke \
  -H "Content-Type: application/json" \
  -d '{"company_name_or_ticker": "Apple"}'
```

## Configuration

### MCP Server Configuration
Located in `.kiro/config/mcp_config.json`:
```json
{
  "mcp": {
    "enabled": true,
    "host": "localhost",
    "port": 8001,
    "max_connections": 100,
    "connection_timeout": 300
  }
}
```

### A2A Configuration
A2A is always enabled when the main application runs. No separate configuration needed.

## Monitoring

All protocols are monitored through:
- Health endpoints: `/health`, `/health/detailed`
- Status endpoint: `/status`
- Metrics endpoint: `/metrics`
- A2A status: `/a2a/status`
- MCP status: `/health/mcp`

## Security Considerations

1. **Authentication**: Ready for API key or OAuth integration
2. **Rate Limiting**: Configurable rate limits per protocol
3. **Input Validation**: All inputs validated against schemas
4. **Audit Trail**: Complete logging of all requests
5. **Error Handling**: No sensitive information in error messages

## Future Enhancements

Potential additions:
- WebSocket support for real-time updates
- GraphQL API
- gRPC for high-performance integrations
- Additional A2A message types (notifications, events)
- Agent-to-agent authentication and authorization