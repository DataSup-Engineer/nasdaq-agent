"""
A2A (Agent-to-Agent) Protocol schema definitions
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum
import uuid


class A2AMessageType(str, Enum):
    """A2A message types"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


class A2ACapabilityType(str, Enum):
    """A2A capability types"""
    ANALYSIS = "analysis"
    DATA_RETRIEVAL = "data_retrieval"
    RESOLUTION = "resolution"
    QUERY = "query"


@dataclass
class A2ACapability:
    """A2A capability definition"""
    id: str
    name: str
    description: str
    capability_type: A2ACapabilityType
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "type": self.capability_type.value,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "version": self.version
        }


@dataclass
class A2AMessage:
    """Base A2A message structure"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: A2AMessageType = A2AMessageType.REQUEST
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    sender_agent_id: Optional[str] = None
    receiver_agent_id: Optional[str] = None
    conversation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "message_id": self.message_id,
            "message_type": self.message_type.value,
            "timestamp": self.timestamp,
            "sender_agent_id": self.sender_agent_id,
            "receiver_agent_id": self.receiver_agent_id,
            "conversation_id": self.conversation_id,
            "metadata": self.metadata
        }


@dataclass
class A2ARequest(A2AMessage):
    """A2A request message"""
    capability_id: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    timeout_seconds: int = 60
    
    def __post_init__(self):
        self.message_type = A2AMessageType.REQUEST
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base = super().to_dict()
        base.update({
            "capability_id": self.capability_id,
            "parameters": self.parameters,
            "timeout_seconds": self.timeout_seconds
        })
        return base
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'A2ARequest':
        """Create from dictionary"""
        return cls(
            message_id=data.get('message_id', str(uuid.uuid4())),
            sender_agent_id=data.get('sender_agent_id'),
            receiver_agent_id=data.get('receiver_agent_id'),
            conversation_id=data.get('conversation_id'),
            capability_id=data.get('capability_id', ''),
            parameters=data.get('parameters', {}),
            timeout_seconds=data.get('timeout_seconds', 60),
            metadata=data.get('metadata', {})
        )


@dataclass
class A2AResponse(A2AMessage):
    """A2A response message"""
    request_id: str = ""
    success: bool = True
    result: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    processing_time_ms: int = 0
    
    def __post_init__(self):
        self.message_type = A2AMessageType.RESPONSE if self.success else A2AMessageType.ERROR
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        base = super().to_dict()
        base.update({
            "request_id": self.request_id,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "processing_time_ms": self.processing_time_ms
        })
        return base
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'A2AResponse':
        """Create from dictionary"""
        return cls(
            message_id=data.get('message_id', str(uuid.uuid4())),
            sender_agent_id=data.get('sender_agent_id'),
            receiver_agent_id=data.get('receiver_agent_id'),
            conversation_id=data.get('conversation_id'),
            request_id=data.get('request_id', ''),
            success=data.get('success', True),
            result=data.get('result', {}),
            error=data.get('error'),
            processing_time_ms=data.get('processing_time_ms', 0),
            metadata=data.get('metadata', {})
        )


# Default A2A capabilities for NASDAQ Stock Agent
ANALYZE_STOCK_CAPABILITY = A2ACapability(
    id="nasdaq.analyze_stock",
    name="Analyze NASDAQ Stock",
    description="Perform comprehensive AI-powered analysis of a NASDAQ stock with investment recommendations",
    capability_type=A2ACapabilityType.ANALYSIS,
    input_schema={
        "type": "object",
        "properties": {
            "company_name_or_ticker": {
                "type": "string",
                "description": "Company name (e.g., 'Apple', 'Microsoft') or ticker symbol (e.g., 'AAPL', 'MSFT')"
            }
        },
        "required": ["company_name_or_ticker"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "ticker": {"type": "string"},
            "company_name": {"type": "string"},
            "recommendation": {"type": "string", "enum": ["Buy", "Hold", "Sell"]},
            "confidence_score": {"type": "number", "minimum": 0, "maximum": 100},
            "current_price": {"type": "number"},
            "price_change_percentage": {"type": "number"},
            "reasoning": {"type": "string"},
            "analysis_id": {"type": "string"}
        }
    }
)

GET_MARKET_DATA_CAPABILITY = A2ACapability(
    id="nasdaq.get_market_data",
    name="Get Market Data",
    description="Retrieve current and historical market data for a NASDAQ stock",
    capability_type=A2ACapabilityType.DATA_RETRIEVAL,
    input_schema={
        "type": "object",
        "properties": {
            "ticker": {
                "type": "string",
                "description": "Stock ticker symbol (e.g., 'AAPL', 'MSFT')"
            },
            "include_historical": {
                "type": "boolean",
                "description": "Whether to include 6-month historical data",
                "default": True
            }
        },
        "required": ["ticker"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "ticker": {"type": "string"},
            "current_price": {"type": "number"},
            "volume": {"type": "number"},
            "daily_high": {"type": "number"},
            "daily_low": {"type": "number"},
            "historical_data": {"type": "array"}
        }
    }
)

RESOLVE_COMPANY_NAME_CAPABILITY = A2ACapability(
    id="nasdaq.resolve_company_name",
    name="Resolve Company Name",
    description="Convert company name to NASDAQ ticker symbol with fuzzy matching",
    capability_type=A2ACapabilityType.RESOLUTION,
    input_schema={
        "type": "object",
        "properties": {
            "company_name": {
                "type": "string",
                "description": "Company name to resolve (e.g., 'Apple Inc.', 'Microsoft Corporation')"
            }
        },
        "required": ["company_name"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "input_name": {"type": "string"},
            "ticker": {"type": "string"},
            "resolved_company_name": {"type": "string"},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1}
        }
    }
)

QUERY_CAPABILITY = A2ACapability(
    id="nasdaq.query",
    name="Natural Language Query",
    description="Process natural language queries about NASDAQ stocks",
    capability_type=A2ACapabilityType.QUERY,
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Natural language query about stocks (e.g., 'Should I buy Apple stock?')"
            }
        },
        "required": ["query"]
    },
    output_schema={
        "type": "object",
        "properties": {
            "response": {"type": "string"},
            "ticker": {"type": "string"},
            "recommendation": {"type": "string"},
            "confidence_score": {"type": "number"}
        }
    }
)

# Default capabilities list
DEFAULT_A2A_CAPABILITIES = [
    ANALYZE_STOCK_CAPABILITY,
    GET_MARKET_DATA_CAPABILITY,
    RESOLVE_COMPANY_NAME_CAPABILITY,
    QUERY_CAPABILITY
]