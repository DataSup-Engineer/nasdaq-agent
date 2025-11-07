"""
Agent information and registry API router
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import logging
from datetime import datetime
from src.services.database import database_service
from src.models.analysis import AgentFactCard

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/agent", tags=["Agent Registry"])


@router.get("/info")
async def get_agent_info() -> Dict[str, Any]:
    """
    Get NASDAQ Stock Agent information
    
    Returns comprehensive information about the agent including capabilities,
    specialization, and registry details.
    """
    try:
        # Get agent fact card from database
        agent_card = await database_service.get_agent_fact_card("nasdaq-stock-agent-v1")
        
        if not agent_card:
            # Return default agent information if not found in database
            return {
                "agent_id": "nasdaq-stock-agent-v1",
                "agent_name": "NASDAQ Stock Agent",
                "agent_domain": "Financial Analysis",
                "agent_specialization": "NASDAQ Stock Analysis and Investment Recommendations",
                "agent_description": "AI-powered agent that provides comprehensive stock analysis and investment recommendations for NASDAQ-listed securities using real-time market data and advanced AI analysis.",
                "agent_capabilities": [
                    "Natural language stock query processing",
                    "Real-time NASDAQ market data retrieval",
                    "6-month historical trend analysis",
                    "AI-powered investment recommendations (Buy/Hold/Sell)",
                    "Risk assessment and confidence scoring",
                    "Company name to ticker symbol resolution",
                    "Comprehensive logging and audit trails"
                ],
                "registry_url": "mongodb://localhost:27017/nasdaq_stock_agent/agent_registry",
                "public_url": "http://localhost:8000/api/v1",
                "status": "active",
                "timestamp": datetime.utcnow().isoformat()
            }
        
        # Convert ObjectId to string if present
        if '_id' in agent_card:
            agent_card['_id'] = str(agent_card['_id'])
        
        # Add status and timestamp
        agent_card['status'] = 'active'
        agent_card['timestamp'] = datetime.utcnow().isoformat()
        
        return agent_card
        
    except Exception as e:
        logger.error(f"Failed to get agent info: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "AGENT_INFO_FAILED",
                "error_message": f"Failed to retrieve agent information: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/capabilities")
async def get_agent_capabilities() -> Dict[str, Any]:
    """
    Get detailed agent capabilities and supported operations
    
    Returns information about what the agent can do, supported query types,
    and operational parameters.
    """
    try:
        capabilities = {
            "natural_language_processing": {
                "supported_queries": [
                    "Company name queries (e.g., 'Apple', 'Microsoft')",
                    "Ticker symbol queries (e.g., 'AAPL', 'MSFT')",
                    "Investment questions (e.g., 'Should I buy Tesla?')",
                    "Analysis requests (e.g., 'Analyze Netflix stock')",
                    "Price inquiries (e.g., 'What's Apple's stock price?')"
                ],
                "supported_companies": "50+ major NASDAQ-listed companies",
                "fuzzy_matching": True,
                "typo_correction": True
            },
            "market_data_analysis": {
                "data_sources": ["Yahoo Finance API"],
                "historical_data_range": "6 months",
                "update_frequency": "Real-time",
                "supported_metrics": [
                    "Current price and daily range",
                    "Trading volume",
                    "Market capitalization",
                    "P/E ratio",
                    "Price change percentage",
                    "Moving averages (20, 50, 200-day)",
                    "RSI (Relative Strength Index)",
                    "Volatility analysis"
                ]
            },
            "ai_analysis": {
                "ai_model": "Anthropic Claude",
                "recommendation_types": ["Buy", "Hold", "Sell"],
                "confidence_scoring": "0-100 scale",
                "analysis_factors": [
                    "Technical indicators",
                    "Price trends and momentum",
                    "Volume analysis",
                    "Fundamental metrics",
                    "Risk assessment"
                ]
            },
            "api_features": {
                "response_format": "JSON",
                "max_concurrent_requests": 50,
                "average_response_time": "< 10 seconds",
                "caching": "Intelligent caching with TTL",
                "rate_limiting": "100 requests per minute",
                "logging": "Comprehensive audit trails"
            },
            "supported_exchanges": ["NASDAQ"],
            "data_retention": "30 days",
            "availability": "24/7"
        }
        
        return {
            "success": True,
            "agent_capabilities": capabilities,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get agent capabilities: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "CAPABILITIES_FAILED",
                "error_message": f"Failed to retrieve capabilities: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/registry")
async def get_registry_info() -> Dict[str, Any]:
    """
    Get agent registry information
    
    Returns information about the agent registry, including storage location
    and registration details.
    """
    try:
        registry_info = {
            "registry_type": "MongoDB",
            "registry_url": "mongodb://localhost:27017/nasdaq_stock_agent/agent_registry",
            "agent_id": "nasdaq-stock-agent-v1",
            "registration_status": "active",
            "last_updated": datetime.utcnow().isoformat(),
            "registry_schema": {
                "agent_id": "Unique identifier for the agent",
                "agent_name": "Human-readable name",
                "agent_domain": "Domain of expertise",
                "agent_specialization": "Specific area of specialization",
                "agent_description": "Detailed description of capabilities",
                "agent_capabilities": "List of specific capabilities",
                "registry_url": "URL of the registry storage",
                "public_url": "Public API endpoint URL"
            }
        }
        
        return {
            "success": True,
            "registry_info": registry_info,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get registry info: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "REGISTRY_INFO_FAILED",
                "error_message": f"Failed to retrieve registry information: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/examples")
async def get_usage_examples() -> Dict[str, Any]:
    """
    Get usage examples and sample queries
    
    Returns example queries and expected responses to help users understand
    how to interact with the agent.
    """
    try:
        examples = {
            "basic_queries": [
                {
                    "query": "Apple",
                    "description": "Simple company name query",
                    "expected_response": "Investment analysis for Apple Inc. (AAPL)"
                },
                {
                    "query": "MSFT",
                    "description": "Direct ticker symbol query", 
                    "expected_response": "Investment analysis for Microsoft Corporation (MSFT)"
                }
            ],
            "natural_language_queries": [
                {
                    "query": "What do you think about Tesla stock?",
                    "description": "Opinion-based investment question",
                    "expected_response": "Comprehensive analysis with Buy/Hold/Sell recommendation"
                },
                {
                    "query": "Should I buy Netflix?",
                    "description": "Direct investment advice question",
                    "expected_response": "Investment recommendation with confidence score and reasoning"
                },
                {
                    "query": "Analyze Amazon stock performance",
                    "description": "Analysis request",
                    "expected_response": "Detailed technical and fundamental analysis"
                }
            ],
            "response_format": {
                "analysis_id": "Unique identifier for the analysis",
                "ticker": "Stock ticker symbol",
                "company_name": "Full company name",
                "current_price": "Current stock price",
                "recommendation": "Buy/Hold/Sell recommendation",
                "confidence_score": "Confidence level (0-100)",
                "reasoning": "Detailed analysis reasoning",
                "key_factors": "List of key factors influencing the recommendation",
                "risk_assessment": "Risk evaluation",
                "processing_time_ms": "Analysis processing time"
            },
            "error_handling": {
                "invalid_company": {
                    "query": "XYZ Company",
                    "response": "Error with suggestions for valid companies"
                },
                "misspelled_name": {
                    "query": "Aple",
                    "response": "Automatic correction to 'Apple' with analysis"
                }
            }
        }
        
        return {
            "success": True,
            "usage_examples": examples,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get usage examples: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error_code": "EXAMPLES_FAILED",
                "error_message": f"Failed to retrieve usage examples: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )