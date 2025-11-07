"""
A2A Capabilities registry and management
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

from .schemas import (
    A2ACapability,
    DEFAULT_A2A_CAPABILITIES,
    A2ACapabilityType
)

logger = logging.getLogger(__name__)


class A2ACapabilities:
    """Registry for A2A capabilities"""
    
    def __init__(self):
        self._capabilities: Dict[str, A2ACapability] = {}
        self.agent_id = "nasdaq-stock-agent"
        self.agent_name = "NASDAQ Stock Agent"
        self.agent_version = "1.0.0"
        self.agent_description = "AI-powered NASDAQ stock analysis and investment recommendations"
        self._initialize_default_capabilities()
    
    def _initialize_default_capabilities(self) -> None:
        """Initialize with default capabilities"""
        for capability in DEFAULT_A2A_CAPABILITIES:
            self.register_capability(capability)
        
        logger.info(f"Initialized A2A capabilities registry with {len(self._capabilities)} capabilities")
    
    def register_capability(self, capability: A2ACapability) -> None:
        """Register a new capability"""
        self._capabilities[capability.id] = capability
        logger.info(f"Registered A2A capability: {capability.id}")
    
    def get_capability(self, capability_id: str) -> Optional[A2ACapability]:
        """Get a specific capability by ID"""
        return self._capabilities.get(capability_id)
    
    def get_all_capabilities(self) -> List[A2ACapability]:
        """Get all registered capabilities"""
        return list(self._capabilities.values())
    
    def get_capabilities_by_type(self, capability_type: A2ACapabilityType) -> List[A2ACapability]:
        """Get capabilities filtered by type"""
        return [
            cap for cap in self._capabilities.values()
            if cap.capability_type == capability_type
        ]
    
    def has_capability(self, capability_id: str) -> bool:
        """Check if a capability is registered"""
        return capability_id in self._capabilities
    
    def get_capability_ids(self) -> List[str]:
        """Get list of all capability IDs"""
        return list(self._capabilities.keys())
    
    def get_agent_manifest(self) -> Dict[str, Any]:
        """Get A2A agent manifest with all capabilities"""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "version": self.agent_version,
            "description": self.agent_description,
            "protocol": "A2A",
            "protocol_version": "1.0",
            "capabilities": [cap.to_dict() for cap in self._capabilities.values()],
            "supported_message_types": ["request", "response", "notification", "error"],
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_capability_manifest(self, capability_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed manifest for a specific capability"""
        capability = self.get_capability(capability_id)
        if not capability:
            return None
        
        return {
            "agent_id": self.agent_id,
            "capability": capability.to_dict(),
            "endpoint": f"/a2a/capabilities/{capability_id}/invoke",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def validate_capability_input(self, capability_id: str, parameters: Dict[str, Any]) -> Optional[str]:
        """Validate input parameters against capability schema"""
        capability = self.get_capability(capability_id)
        if not capability:
            return f"Capability '{capability_id}' not found"
        
        schema = capability.input_schema
        required = schema.get('required', [])
        properties = schema.get('properties', {})
        
        # Check required parameters
        for param in required:
            if param not in parameters:
                return f"Missing required parameter: {param}"
        
        # Basic type validation
        for param_name, param_value in parameters.items():
            if param_name in properties:
                expected_type = properties[param_name].get('type')
                
                if expected_type == 'string' and not isinstance(param_value, str):
                    return f"Parameter '{param_name}' must be a string"
                elif expected_type == 'boolean' and not isinstance(param_value, bool):
                    return f"Parameter '{param_name}' must be a boolean"
                elif expected_type == 'number' and not isinstance(param_value, (int, float)):
                    return f"Parameter '{param_name}' must be a number"
        
        return None  # No validation errors
    
    def get_capabilities_summary(self) -> Dict[str, Any]:
        """Get summary of capabilities"""
        return {
            "total_capabilities": len(self._capabilities),
            "capabilities_by_type": {
                cap_type.value: len(self.get_capabilities_by_type(cap_type))
                for cap_type in A2ACapabilityType
            },
            "capability_ids": self.get_capability_ids(),
            "agent_id": self.agent_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def unregister_capability(self, capability_id: str) -> bool:
        """Unregister a capability"""
        if capability_id in self._capabilities:
            del self._capabilities[capability_id]
            logger.info(f"Unregistered A2A capability: {capability_id}")
            return True
        return False
    
    def clear_capabilities(self) -> None:
        """Clear all capabilities"""
        self._capabilities.clear()
        logger.info("Cleared A2A capabilities registry")


# Global capabilities registry instance
a2a_capabilities = A2ACapabilities()