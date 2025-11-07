"""
A2A (Agent-to-Agent) Protocol API router
Supports both custom A2A implementation and official agent-protocol
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
import logging
from datetime import datetime

from src.a2a.schemas import A2ARequest, A2AResponse
from src.a2a.capabilities import a2a_capabilities
from src.a2a.handler import a2a_handler
from src.a2a.agent_protocol_adapter import nasdaq_agent, AGENT_PROTOCOL_AVAILABLE

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/a2a", tags=["A2A Protocol"])


@router.get("/manifest")
async def get_agent_manifest() -> Dict[str, Any]:
    """
    Get A2A agent manifest
    
    Returns the agent's capabilities, supported message types, and protocol information
    for agent-to-agent discovery and integration.
    """
    try:
        manifest = a2a_capabilities.get_agent_manifest()
        return manifest
    except Exception as e:
        logger.error(f"Failed to get A2A manifest: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to get agent manifest: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/capabilities")
async def list_capabilities() -> Dict[str, Any]:
    """
    List all available A2A capabilities
    
    Returns a list of all capabilities this agent can perform, including
    their IDs, descriptions, and input/output schemas.
    """
    try:
        capabilities = a2a_capabilities.get_all_capabilities()
        
        return {
            "success": True,
            "agent_id": a2a_capabilities.agent_id,
            "capabilities": [cap.to_dict() for cap in capabilities],
            "total_count": len(capabilities),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to list A2A capabilities: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to list capabilities: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/capabilities/{capability_id}")
async def get_capability_details(capability_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific capability
    
    Returns the complete capability manifest including input/output schemas,
    description, and invocation endpoint.
    """
    try:
        manifest = a2a_capabilities.get_capability_manifest(capability_id)
        
        if not manifest:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": f"Capability '{capability_id}' not found",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        return {
            "success": True,
            "manifest": manifest,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get capability details: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to get capability details: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/request")
async def handle_a2a_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle an A2A protocol request
    
    Processes agent-to-agent requests according to the A2A protocol specification.
    Accepts requests with capability_id and parameters, returns structured responses.
    """
    try:
        # Parse A2A request
        a2a_request = A2ARequest.from_dict(request_data)
        
        # Set receiver agent ID
        a2a_request.receiver_agent_id = a2a_capabilities.agent_id
        
        # Handle the request
        a2a_response = await a2a_handler.handle_request(a2a_request)
        
        # Return response as dictionary
        return a2a_response.to_dict()
        
    except Exception as e:
        logger.error(f"A2A request handling failed: {e}")
        
        # Create error response
        error_response = A2AResponse(
            request_id=request_data.get('message_id', 'unknown'),
            sender_agent_id=a2a_capabilities.agent_id,
            receiver_agent_id=request_data.get('sender_agent_id'),
            conversation_id=request_data.get('conversation_id'),
            success=False,
            result={},
            error=f"Request handling failed: {str(e)}",
            processing_time_ms=0
        )
        
        return error_response.to_dict()


@router.post("/capabilities/{capability_id}/invoke")
async def invoke_capability(capability_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke a specific capability directly
    
    Simplified endpoint for invoking a capability without full A2A message structure.
    Useful for quick testing and simple integrations.
    """
    try:
        # Create A2A request
        a2a_request = A2ARequest(
            capability_id=capability_id,
            parameters=parameters,
            receiver_agent_id=a2a_capabilities.agent_id
        )
        
        # Handle the request
        a2a_response = await a2a_handler.handle_request(a2a_request)
        
        # Return simplified response
        if a2a_response.success:
            return {
                "success": True,
                "result": a2a_response.result,
                "processing_time_ms": a2a_response.processing_time_ms,
                "timestamp": a2a_response.timestamp
            }
        else:
            return {
                "success": False,
                "error": a2a_response.error,
                "processing_time_ms": a2a_response.processing_time_ms,
                "timestamp": a2a_response.timestamp
            }
        
    except Exception as e:
        logger.error(f"Capability invocation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Capability invocation failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/status")
async def get_a2a_status() -> Dict[str, Any]:
    """
    Get A2A protocol handler status
    
    Returns status information about the A2A handler including initialization state,
    available capabilities, and performance metrics.
    """
    try:
        handler_status = a2a_handler.get_handler_status()
        capabilities_summary = a2a_capabilities.get_capabilities_summary()
        
        return {
            "success": True,
            "handler_status": handler_status,
            "capabilities_summary": capabilities_summary,
            "protocol": "A2A",
            "protocol_version": "1.0",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get A2A status: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to get A2A status: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/health")
async def a2a_health_check() -> Dict[str, Any]:
    """
    A2A protocol health check
    
    Simple health check endpoint for monitoring A2A protocol availability.
    """
    try:
        is_healthy = a2a_handler.is_initialized
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "protocol": "A2A",
            "agent_id": a2a_capabilities.agent_id,
            "capabilities_count": len(a2a_capabilities.get_all_capabilities()),
            "agent_protocol_available": AGENT_PROTOCOL_AVAILABLE,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"A2A health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/agent")
async def get_agent_info() -> Dict[str, Any]:
    """
    Get agent information (agent-protocol standard)
    
    Returns agent information following the agent-protocol specification.
    Compatible with agent-protocol clients and frameworks.
    """
    try:
        agent_info = nasdaq_agent.get_agent_info()
        agent_info['agent_protocol_available'] = AGENT_PROTOCOL_AVAILABLE
        
        return {
            "success": True,
            "agent": agent_info,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get agent info: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Failed to get agent info: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/tasks")
async def create_task(task_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create and execute a task (agent-protocol standard)
    
    Executes a task using the agent-protocol standard interface.
    Compatible with agent-protocol clients and frameworks.
    
    Request body can be:
    - {"action": "analyze_stock", "parameters": {"company_name_or_ticker": "Apple"}}
    - {"action": "query", "parameters": {"query": "Should I buy Tesla?"}}
    - Or a natural language string that will be treated as a query
    """
    try:
        # Execute task using the agent protocol adapter
        result = await nasdaq_agent.execute_task(task_input)
        
        return {
            "task_id": f"task_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "status": "completed" if result.get('success') else "failed",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Task execution failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )