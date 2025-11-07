"""
A2A (Agent-to-Agent) Protocol implementation for NASDAQ Stock Agent
Supports both custom A2A implementation and official agent-protocol package
"""

# Always available - no external dependencies
from .schemas import A2AMessage, A2ARequest, A2AResponse, A2ACapability

# Conditionally import modules that have dependencies
try:
    from .handler import A2AHandler, a2a_handler
    from .capabilities import A2ACapabilities, a2a_capabilities
    from .agent_protocol_adapter import (
        nasdaq_agent,
        NASDAQStockAgent,
        AGENT_PROTOCOL_AVAILABLE,
        create_agent_protocol_server
    )
    
    __all__ = [
        'A2AMessage',
        'A2ARequest',
        'A2AResponse',
        'A2ACapability',
        'A2AHandler',
        'a2a_handler',
        'A2ACapabilities',
        'a2a_capabilities',
        'nasdaq_agent',
        'NASDAQStockAgent',
        'AGENT_PROTOCOL_AVAILABLE',
        'create_agent_protocol_server'
    ]
except ImportError as e:
    # If dependencies are not available, only export basic schemas
    __all__ = [
        'A2AMessage',
        'A2ARequest',
        'A2AResponse',
        'A2ACapability'
    ]