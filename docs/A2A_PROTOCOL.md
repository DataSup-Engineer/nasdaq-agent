# A2A (Agent-to-Agent) Protocol

The NASDAQ Stock Agent supports the A2A (Agent-to-Agent) protocol for direct agent-to-agent communication and capability invocation.

## Overview

A2A is a protocol that enables AI agents to discover, communicate with, and invoke capabilities of other agents. The NASDAQ Stock Agent exposes its stock analysis capabilities through standardized A2A interfaces.

The implementation supports:
- **Custom A2A Protocol**: REST-based agent-to-agent communication with custom message format
- **Official agent-protocol**: Integration with the official `agent-protocol` Python package for standardized agent communication

## Installation

To use the official agent-protocol package:

```bash
pip install agent-protocol
```

The agent will work with or without the package, but having it installed enables full agent-protocol compatibility.

## Key Features

- **Agent Discovery**: Get agent manifest with all available capabilities
- **Capability Invocation**: Execute specific capabilities with structured requests
- **Standardized Messaging**: Use A2A message format for requests and responses
- **Audit Trail**: All A2A requests are logged to the same audit trail as REST API requests

## Running the Agent Protocol Server

### Option 1: Integrated with Main Application
```bash
python main.py
```
Access A2A endpoints at `http://localhost:8000/a2a/`

### Option 2: Standalone Agent Protocol Server
```bash
python agent_protocol_server.py
```
Runs a dedicated agent-protocol server on port 8001 (requires `agent-protocol` package)

## Endpoints

### Agent Protocol Standard Endpoints

#### Get Agent Information
```
GET /a2a/agent
```

Returns agent information following the agent-protocol specification.

#### Create and Execute Task
```
POST /a2a/tasks
```

Execute a task using the agent-protocol standard.

**Request Body:**
```json
{
  "action": "analyze_stock",
  "parameters": {
    "company_name_or_ticker": "Apple"
  }
}
```

**Response:**
```json
{
  "task_id": "task_20241107_123456",
  "status": "completed",
  "result": {
    "success": true,
    "output": {
      "ticker": "AAPL",
      "recommendation": "Buy",
      "confidence_score": 85.5
    }
  }
}
```

### Custom A2A Protocol Endpoints

### Get Agent Manifest
```
GET /a2a/manifest
```

Returns the agent's capabilities, supported message types, and protocol information.

**Response:**
```json
{
  "agent_id": "nasdaq-stock-agent",
  "agent_name": "NASDAQ Stock Agent",
  "version": "1.0.0",
  "description": "AI-powered NASDAQ stock analysis and investment recommendations",
  "protocol": "A2A",
  "protocol_version": "1.0",
  "capabilities": [...],
  "supported_message_types": ["request", "response", "notification", "error"]
}
```

### List Capabilities
```
GET /a2a/capabilities
```

Returns all available capabilities with their schemas.

### Get Capability Details
```
GET /a2a/capabilities/{capability_id}
```

Returns detailed information about a specific capability.

### Send A2A Request
```
POST /a2a/request
```

Send a full A2A protocol request.

**Request Body:**
```json
{
  "message_id": "unique-message-id",
  "message_type": "request",
  "sender_agent_id": "your-agent-id",
  "capability_id": "nasdaq.analyze_stock",
  "parameters": {
    "company_name_or_ticker": "Apple"
  },
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "message_id": "response-message-id",
  "message_type": "response",
  "request_id": "original-request-id",
  "sender_agent_id": "nasdaq-stock-agent",
  "receiver_agent_id": "your-agent-id",
  "success": true,
  "result": {
    "ticker": "AAPL",
    "company_name": "Apple Inc.",
    "recommendation": "Buy",
    "confidence_score": 85.5,
    "current_price": 175.43,
    "reasoning": "..."
  },
  "processing_time_ms": 1234
}
```

### Invoke Capability (Simplified)
```
POST /a2a/capabilities/{capability_id}/invoke
```

Simplified endpoint for quick capability invocation without full A2A message structure.

**Request Body:**
```json
{
  "company_name_or_ticker": "Apple"
}
```

## Available Capabilities

### 1. nasdaq.analyze_stock
Perform comprehensive AI-powered analysis of a NASDAQ stock.

**Input:**
- `company_name_or_ticker` (string, required): Company name or ticker symbol

**Output:**
- `ticker`: Stock ticker symbol
- `company_name`: Full company name
- `recommendation`: Buy/Hold/Sell
- `confidence_score`: 0-100
- `current_price`: Current stock price
- `price_change_percentage`: Price change percentage
- `reasoning`: Detailed analysis reasoning
- `analysis_id`: Unique analysis identifier

### 2. nasdaq.get_market_data
Retrieve current and historical market data.

**Input:**
- `ticker` (string, required): Stock ticker symbol
- `include_historical` (boolean, optional): Include 6-month historical data (default: true)

**Output:**
- `ticker`: Stock ticker symbol
- `current_price`: Current price
- `volume`: Trading volume
- `daily_high`: Daily high price
- `daily_low`: Daily low price
- `historical_data`: Historical price data (if requested)

### 3. nasdaq.resolve_company_name
Convert company name to ticker symbol.

**Input:**
- `company_name` (string, required): Company name to resolve

**Output:**
- `input_name`: Original input name
- `ticker`: Resolved ticker symbol
- `resolved_company_name`: Full company name
- `confidence`: Resolution confidence (0-1)

### 4. nasdaq.query
Process natural language queries about stocks.

**Input:**
- `query` (string, required): Natural language query

**Output:**
- `response`: Natural language response
- `ticker`: Identified ticker symbol
- `recommendation`: Investment recommendation
- `confidence_score`: Confidence score

## Example Usage

### Using the Official agent-protocol Package

```python
from agent_protocol import Agent

# Connect to the NASDAQ Stock Agent
agent = Agent(base_url="http://localhost:8001")

# Get agent information
agent_info = await agent.get_agent()
print(f"Connected to: {agent_info['name']}")

# Create and execute a task
task = await agent.create_task({
    "action": "analyze_stock",
    "parameters": {
        "company_name_or_ticker": "Apple"
    }
})

print(f"Task ID: {task['task_id']}")
print(f"Result: {task['result']}")
```

### Python Example (REST API)
```python
import requests

# Get agent manifest
manifest = requests.get("http://localhost:8000/a2a/manifest").json()
print(f"Agent: {manifest['agent_name']}")
print(f"Capabilities: {len(manifest['capabilities'])}")

# Invoke capability (simplified)
response = requests.post(
    "http://localhost:8000/a2a/capabilities/nasdaq.analyze_stock/invoke",
    json={"company_name_or_ticker": "Apple"}
)
result = response.json()
print(f"Recommendation: {result['result']['recommendation']}")
print(f"Confidence: {result['result']['confidence_score']}%")

# Send full A2A request
a2a_request = {
    "message_id": "req-123",
    "sender_agent_id": "my-agent",
    "capability_id": "nasdaq.get_market_data",
    "parameters": {
        "ticker": "AAPL",
        "include_historical": True
    }
}
response = requests.post(
    "http://localhost:8000/a2a/request",
    json=a2a_request
)
result = response.json()
print(f"Current Price: ${result['result']['current_price']}")
```

### JavaScript Example
```javascript
// Get agent manifest
const manifest = await fetch('http://localhost:8000/a2a/manifest')
  .then(r => r.json());
console.log(`Agent: ${manifest.agent_name}`);

// Invoke capability
const response = await fetch(
  'http://localhost:8000/a2a/capabilities/nasdaq.analyze_stock/invoke',
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ company_name_or_ticker: 'Microsoft' })
  }
).then(r => r.json());

console.log(`Recommendation: ${response.result.recommendation}`);
console.log(`Confidence: ${response.result.confidence_score}%`);
```

## Status and Health

### Get A2A Status
```
GET /a2a/status
```

Returns A2A handler status and capabilities summary.

### Health Check
```
GET /a2a/health
```

Simple health check for A2A protocol availability.

## Integration with Other Protocols

The NASDAQ Stock Agent supports both A2A and MCP (Model Context Protocol):

- **A2A**: Direct agent-to-agent communication via REST API
- **MCP**: Standardized tool interface for AI agent frameworks

Both protocols provide access to the same underlying capabilities and share the same audit trail.

## Error Handling

A2A responses include error information when requests fail:

```json
{
  "message_type": "error",
  "success": false,
  "error": "Error description",
  "processing_time_ms": 123
}
```

Common error scenarios:
- Capability not found
- Invalid parameters
- Service unavailable
- Timeout exceeded

## Logging and Audit Trail

All A2A requests are logged to MongoDB with:
- Request parameters
- Response data
- Processing time
- Sender agent ID
- Conversation ID
- Timestamp

Logs are retained for 30 days and can be queried through the logging API.