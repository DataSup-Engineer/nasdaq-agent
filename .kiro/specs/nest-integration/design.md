# NEST Integration Design

## Overview

This document describes the design for integrating the NASDAQ Stock Agent with the NANDA NEST framework. The design follows Option 1: Minimal Integration, which adds NEST as an additional interface while preserving the existing FastAPI REST API.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NASDAQ Stock Agent                        │
│                                                              │
│  ┌────────────────────┐         ┌─────────────────────┐    │
│  │   FastAPI Server   │         │   NEST A2A Server   │    │
│  │    (Port 8000)     │         │    (Port 6000)      │    │
│  └─────────┬──────────┘         └──────────┬──────────┘    │
│            │                               │                │
│            │                               │                │
│            ├───────────┬───────────────────┤                │
│            │           │                   │                │
│  ┌─────────▼───────────▼───────────────────▼──────────┐    │
│  │         Core Analysis Services                      │    │
│  │  - comprehensive_analysis_service                   │    │
│  │  - market_data_service                              │    │
│  │  - enhanced_nlp_service                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
         │                                    │
         │                                    │
         ▼                                    ▼
   REST Clients                      NANDA Registry
   (curl, web apps)                  (registry.chat39.com:6900)
                                            │
                                            ▼
                                     Other NEST Agents
```

### Component Architecture

```
src/
├── nest/                          # NEST integration components
│   ├── __init__.py
│   ├── adapter.py                 # NEST adapter (wraps NANDA class)
│   ├── agent_bridge.py            # A2A message handler
│   ├── agent_logic.py             # Translates A2A to analysis logic
│   └── config.py                  # NEST configuration
├── api/                           # Existing FastAPI application
│   ├── app.py                     # FastAPI app (unchanged)
│   └── routers/
│       ├── agent.py               # Agent facts endpoint (enhanced)
│       └── ...
├── services/                      # Core services (unchanged)
│   ├── investment_analysis.py
│   ├── market_data_service.py
│   └── ...
└── main.py                        # Application entry point (modified)
```

## Components

### 1. NEST Configuration (`src/nest/config.py`)

**Purpose:** Manage NEST-specific configuration from environment variables.

**Key Attributes:**
- `nest_enabled`: Boolean flag to enable/disable NEST
- `nest_port`: Port for A2A server (default: 6000)
- `nest_registry_url`: NANDA Registry URL
- `nest_public_url`: Public URL for agent registration
- `agent_id`: Unique identifier ("nasdaq-stock-agent")
- `agent_name`: Display name ("NASDAQ Stock Agent")
- `domain`: "financial analysis"
- `specialization`: "NASDAQ stock analysis and investment recommendations"

**Methods:**
- `from_env()`: Load configuration from environment variables
- `validate()`: Validate configuration completeness
- `should_enable_nest()`: Determine if NEST should be enabled

### 2. Agent Logic Adapter (`src/nest/agent_logic.py`)

**Purpose:** Translate A2A messages to stock analysis requests and format responses.

**Key Functions:**

```python
async def process_a2a_message(message: str, conversation_id: str) -> str:
    """
    Process incoming A2A message and return response.
    
    Handles:
    - Stock queries: "AAPL", "Apple", "What about Tesla?"
    - Help commands: "/help", "/info"
    - Status commands: "/status", "/ping"
    """
```

**Message Flow:**
1. Parse incoming A2A message text
2. Detect message type (stock query, command, etc.)
3. For stock queries:
   - Extract ticker/company name using enhanced_nlp_service
   - Call comprehensive_analysis_service
   - Format analysis result as readable text
4. For commands:
   - Execute command (help, status, etc.)
   - Return formatted response
5. Return response string

### 3. Agent Bridge (`src/nest/agent_bridge.py`)

**Purpose:** Implement A2AServer interface from python_a2a library.

**Based on:** NEST's `SimpleAgentBridge` pattern

**Key Methods:**

```python
class StockAgentBridge(A2AServer):
    def handle_message(self, msg: Message) -> Message:
        """Handle incoming A2A messages"""
        # 1. Extract text content
        # 2. Check for special prefixes (@, #, /)
        # 3. Route to appropriate handler
        # 4. Return formatted Message response
    
    def _handle_stock_query(self, query: str, msg: Message, conv_id: str) -> Message:
        """Handle stock analysis queries"""
        # Call agent_logic.process_a2a_message()
        # Format as Message response
    
    def _handle_agent_message(self, text: str, msg: Message, conv_id: str) -> Message:
        """Handle @agent-id messages for A2A communication"""
        # Parse target agent and message
        # Look up agent in registry
        # Forward message using A2AClient
    
    def _handle_command(self, text: str, msg: Message, conv_id: str) -> Message:
        """Handle system commands (/help, /status, etc.)"""
        # Execute command
        # Return formatted response
    
    def _lookup_agent(self, agent_id: str) -> Optional[str]:
        """Look up agent URL in NANDA Registry"""
        # Query registry at {registry_url}/lookup/{agent_id}
        # Return agent_url or None
    
    def _create_response(self, original_msg: Message, conv_id: str, text: str) -> Message:
        """Create A2A response message"""
        # Create Message with MessageRole.AGENT
        # Include parent_message_id
        # Prefix with [nasdaq-stock-agent]
```

### 4. NEST Adapter (`src/nest/adapter.py`)

**Purpose:** Wrap NANDA class and manage A2A server lifecycle.

**Key Methods:**

```python
class NESTAdapter:
    def __init__(self, config: NESTConfig):
        """Initialize NEST adapter with configuration"""
        self.config = config
        self.bridge = StockAgentBridge(
            agent_id=config.agent_id,
            agent_logic=process_a2a_message,
            registry_url=config.nest_registry_url
        )
        self.server_process = None
    
    async def start_async(self, register: bool = True):
        """Start A2A server in background thread"""
        # Register with NANDA Registry if enabled
        # Start python_a2a server in separate thread
        # Monitor server health
    
    async def stop_async(self):
        """Stop A2A server gracefully"""
        # Deregister from NANDA Registry
        # Stop server thread
        # Clean up resources
    
    def _register(self):
        """Register agent with NANDA Registry"""
        # POST to {registry_url}/register
        # Payload: {"agent_id": ..., "agent_url": ...}
        # Retry logic with exponential backoff
    
    def _deregister(self):
        """Deregister agent from NANDA Registry"""
        # DELETE {registry_url}/agents/{agent_id}
    
    async def get_status(self) -> Dict[str, Any]:
        """Get NEST adapter status"""
        # Return server status, registration status, etc.
    
    def is_running(self) -> bool:
        """Check if A2A server is running"""
```

### 5. Main Application Integration (`main.py`)

**Purpose:** Initialize both FastAPI and NEST servers.

**Modifications:**

```python
# Global NEST adapter instance
_nest_adapter: Optional[NESTAdapter] = None

async def initialize_nest():
    """Initialize NEST integration if enabled"""
    global _nest_adapter
    
    try:
        # Load NEST configuration
        nest_config = NESTConfig.from_env()
        
        # Check if NEST should be enabled
        if not nest_config.should_enable_nest():
            logger.info("NEST integration is disabled")
            return None
        
        # Validate configuration
        is_valid, errors = nest_config.validate()
        if not is_valid:
            logger.error(f"NEST configuration invalid: {errors}")
            return None
        
        # Create NEST adapter
        _nest_adapter = NESTAdapter(config=nest_config)
        
        # Start NEST adapter
        await _nest_adapter.start_async(register=True)
        
        logger.info(f"NEST adapter started on port {nest_config.nest_port}")
        return _nest_adapter
        
    except ImportError as e:
        logger.warning(f"NEST integration requires python-a2a: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to initialize NEST: {e}")
        return None

async def shutdown_nest():
    """Shutdown NEST integration"""
    global _nest_adapter
    
    if _nest_adapter and _nest_adapter.is_running():
        await _nest_adapter.stop_async()
        _nest_adapter = None

# Add to FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await initialize_nest()
    yield
    # Shutdown
    await shutdown_nest()
```

### 6. Enhanced Agent Facts Endpoint

**Purpose:** Provide agent metadata for NEST discovery.

**Enhancements to `src/api/routers/agent.py`:**

```python
@router.get("/info")
async def get_agent_info() -> Dict[str, Any]:
    """Get agent information including NEST metadata"""
    return {
        "agent_id": "nasdaq-stock-agent",
        "agent_name": "NASDAQ Stock Agent",
        "agent_domain": "Financial Analysis",
        "agent_specialization": "NASDAQ Stock Analysis and Investment Recommendations",
        "agent_description": "AI-powered agent that provides comprehensive stock analysis...",
        "agent_capabilities": [
            "Natural language stock query processing",
            "Real-time NASDAQ market data retrieval",
            "6-month historical trend analysis",
            "AI-powered investment recommendations (Buy/Hold/Sell)",
            "Risk assessment and confidence scoring",
            "Company name to ticker symbol resolution"
        ],
        "supported_operations": [
            {
                "operation": "stock_analysis",
                "description": "Analyze a stock and provide investment recommendation",
                "example": "AAPL" or "What about Tesla stock?"
            },
            {
                "operation": "ticker_resolution",
                "description": "Resolve company name to ticker symbol",
                "example": "Apple" -> "AAPL"
            }
        ],
        "a2a_endpoint": f"{public_url}/a2a" if nest_enabled else None,
        "rest_endpoint": "http://localhost:8000/api/v1",
        "status": "active",
        "nest_enabled": nest_enabled,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Data Models

### A2A Message Format

**Incoming Message:**
```json
{
  "role": "user",
  "content": {
    "type": "text",
    "text": "What do you think about Apple stock?"
  },
  "conversation_id": "conv-123",
  "message_id": "msg-456"
}
```

**Outgoing Response:**
```json
{
  "role": "agent",
  "content": {
    "type": "text",
    "text": "[nasdaq-stock-agent] Apple Inc. (AAPL) Analysis:\n\nCurrent Price: $178.45 (+1.2%)\nRecommendation: Buy (Confidence: 85%)\n\nKey Factors:\n- Strong upward trend over 6 months\n- Price above key moving averages\n- Solid fundamentals with P/E of 28.5\n\nRisk Assessment: Moderate risk due to high valuation..."
  },
  "conversation_id": "conv-123",
  "parent_message_id": "msg-456",
  "message_id": "msg-789"
}
```

### Registry Registration Format

**Registration Request:**
```json
{
  "agent_id": "nasdaq-stock-agent",
  "agent_url": "http://your-public-ip:6000/a2a",
  "api_url": "http://your-public-ip:8000/api/v1",
  "agent_facts_url": "http://your-public-ip:8000/api/v1/agent/info"
}
```

## Configuration

### Environment Variables

```bash
# NEST Integration
NEST_ENABLED=true                                    # Enable NEST integration
NEST_PORT=6000                                       # A2A server port
NEST_REGISTRY_URL=http://registry.chat39.com:6900   # NANDA Registry URL
NEST_PUBLIC_URL=http://your-public-ip:6000          # Public A2A endpoint

# Agent Identity
NEST_AGENT_ID=nasdaq-stock-agent                    # Unique agent identifier
NEST_AGENT_NAME=NASDAQ Stock Agent                  # Display name
NEST_DOMAIN=financial analysis                      # Domain of expertise
NEST_SPECIALIZATION=NASDAQ stock analysis and investment recommendations

# Existing Configuration (unchanged)
ANTHROPIC_API_KEY=sk-ant-...
PORT=8000
```

## Error Handling

### Error Scenarios

1. **NEST Initialization Failure**
   - Log error with details
   - Continue with REST-only mode
   - Set nest_status to "disabled"

2. **Registry Registration Failure**
   - Retry up to 3 times with exponential backoff (1s, 2s, 4s)
   - Log warning if all retries fail
   - Continue operation (agent still works, just not discoverable)

3. **A2A Message Processing Error**
   - Catch exception in agent_logic
   - Return error message in A2A format
   - Log error with stack trace
   - Don't crash the server

4. **Agent Lookup Failure**
   - Return "Agent {agent-id} not found" message
   - Log warning
   - Suggest using /list command to see available agents

5. **python_a2a Not Installed**
   - Detect ImportError during initialization
   - Log warning about missing dependency
   - Disable NEST features
   - Continue with REST-only mode

## Testing Strategy

### Unit Tests

1. **NESTConfig Tests**
   - Test configuration loading from environment
   - Test validation logic
   - Test should_enable_nest() conditions

2. **Agent Logic Tests**
   - Test stock query parsing
   - Test command handling
   - Test response formatting
   - Test error handling

3. **Agent Bridge Tests**
   - Test message routing
   - Test A2A message creation
   - Test agent lookup
   - Test error responses

### Integration Tests

1. **NEST Adapter Tests**
   - Test server startup/shutdown
   - Test registry registration
   - Test concurrent FastAPI + A2A operation

2. **End-to-End Tests**
   - Test A2A stock query flow
   - Test @agent-id forwarding
   - Test command execution
   - Test error scenarios

### Manual Testing

1. **Local Testing**
   ```bash
   # Start agent with NEST enabled
   NEST_ENABLED=true NEST_PORT=6000 python main.py
   
   # Test A2A endpoint
   curl -X POST http://localhost:6000/a2a \
     -H "Content-Type: application/json" \
     -d '{"content":{"text":"AAPL","type":"text"},"role":"user","conversation_id":"test"}'
   ```

2. **Registry Integration Testing**
   - Register with actual NANDA Registry
   - Verify agent appears in registry listing
   - Test agent lookup from another agent
   - Test deregistration on shutdown

## Security Considerations

1. **Input Validation**
   - Validate all A2A message content
   - Sanitize user input before processing
   - Prevent injection attacks

2. **Rate Limiting**
   - Apply same rate limits to A2A as REST API
   - Track requests per conversation_id
   - Implement backpressure if overloaded

3. **Authentication** (Future Enhancement)
   - Consider adding agent-to-agent authentication
   - Verify sender identity in A2A messages
   - Use signed messages for sensitive operations

## Performance Considerations

1. **Concurrent Operation**
   - Run A2A server in separate thread
   - Use asyncio for non-blocking operations
   - Share service instances between FastAPI and NEST

2. **Resource Management**
   - Reuse existing service instances
   - Don't duplicate analysis logic
   - Clean up resources on shutdown

3. **Monitoring**
   - Track A2A request count and latency
   - Monitor registry connection health
   - Alert on NEST failures

## Deployment

### Docker Deployment

```dockerfile
# Expose both ports
EXPOSE 8000 6000

# Install python-a2a
RUN pip install python-a2a

# Set NEST environment variables
ENV NEST_ENABLED=true
ENV NEST_PORT=6000
ENV NEST_REGISTRY_URL=http://registry.chat39.com:6900
```

### AWS EC2 Deployment

1. Open security group for port 6000
2. Set NEST_PUBLIC_URL to EC2 public IP
3. Configure environment variables
4. Start application with NEST enabled

## Future Enhancements

1. **MCP Integration**
   - Add MCP server support using NEST's mcp_client
   - Enable #nanda:server-name queries
   - Integrate with MCP registry

2. **Advanced A2A Features**
   - Support for multi-turn conversations
   - Context preservation across messages
   - Streaming responses for long analyses

3. **Agent Collaboration**
   - Forward complex queries to specialized agents
   - Aggregate responses from multiple agents
   - Implement agent workflows

4. **Telemetry**
   - Integrate NEST's telemetry system
   - Track A2A message metrics
   - Monitor agent network health
