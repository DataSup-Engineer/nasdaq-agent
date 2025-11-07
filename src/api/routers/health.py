"""
Health check and system status API router
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging
from datetime import datetime
from src.services.logging_middleware import monitoring_service, performance_monitor
from src.agents.stock_analysis_agent import agent_orchestrator
from src.services.market_data_service import market_data_service
from src.services.investment_analysis import comprehensive_analysis_service
from src.core.dependencies import get_mcp_server
from src.a2a.handler import a2a_handler

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health & Status"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint
    
    Returns simple health status for load balancers and monitoring systems.
    """
    try:
        return {
            "status": "healthy",
            "service": "NASDAQ Stock Agent",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """
    Detailed health check with service status
    
    Returns comprehensive health information for all system components.
    """
    try:
        # Get comprehensive system status
        system_status = await monitoring_service.get_comprehensive_status()
        
        return {
            "overall_status": system_status.get("status", "unknown"),
            "system_health": system_status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/status")
async def system_status() -> Dict[str, Any]:
    """
    Get comprehensive system status and metrics
    
    Returns detailed information about system performance, health, and metrics.
    """
    try:
        # Get performance metrics
        performance_metrics = await performance_monitor.get_metrics()
        
        # Get agent health
        agent_health = await agent_orchestrator.get_health_status()
        
        # Get market data service health
        market_health = await market_data_service.get_service_health()
        
        # Get analysis service health
        analysis_health = await comprehensive_analysis_service.get_service_health()
        
        # Get MCP server health
        try:
            mcp_server = await get_mcp_server()
            mcp_health = mcp_server.get_health_status() if mcp_server else {"status": "not_available"}
        except Exception:
            mcp_health = {"status": "error", "message": "Failed to get MCP server status"}
        
        # Get A2A handler health
        try:
            a2a_health = a2a_handler.get_handler_status()
        except Exception:
            a2a_health = {"status": "error", "message": "Failed to get A2A handler status"}
        
        return {
            "service": "NASDAQ Stock Agent",
            "version": "1.0.0",
            "status": "operational",
            "performance_metrics": performance_metrics,
            "service_health": {
                "agent_orchestrator": agent_health,
                "market_data_service": market_health,
                "analysis_service": analysis_health,
                "mcp_server": mcp_health,
                "a2a_handler": a2a_health
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Status check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Get system performance metrics
    
    Returns real-time performance metrics including request counts, response times,
    error rates, and cache statistics.
    """
    try:
        metrics = await performance_monitor.get_metrics()
        
        return {
            "success": True,
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Metrics retrieval failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/metrics/reset")
async def reset_metrics() -> Dict[str, Any]:
    """
    Reset performance metrics
    
    Resets all performance counters and metrics to zero. Useful for testing
    or starting fresh metric collection periods.
    """
    try:
        await performance_monitor.reset_metrics()
        
        return {
            "success": True,
            "message": "Performance metrics have been reset",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to reset metrics: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Metrics reset failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/mcp")
async def mcp_server_status() -> Dict[str, Any]:
    """
    Get MCP (Model Context Protocol) server status
    
    Returns detailed information about the MCP server including available tools,
    connection status, and performance metrics.
    """
    try:
        mcp_server = await get_mcp_server()
        
        if not mcp_server:
            return {
                "status": "not_available",
                "message": "MCP server not initialized",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Get comprehensive MCP server status
        server_status = mcp_server.get_server_status()
        health_status = mcp_server.get_health_status()
        
        # Validate tool schemas
        tool_validation = await mcp_server.validate_tool_schemas()
        
        return {
            "success": True,
            "server_status": server_status,
            "health_status": health_status,
            "tool_validation": tool_validation,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get MCP server status: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"MCP server status check failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )