"""
A2A Request Handler for processing agent-to-agent requests
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from .schemas import A2ARequest, A2AResponse
from .capabilities import A2ACapabilities, a2a_capabilities
from agents.stock_analysis_agent import agent_orchestrator
from services.logging_service import logging_service

logger = logging.getLogger(__name__)


class A2AHandler:
    """Handler for A2A protocol requests"""
    
    def __init__(self, capabilities: Optional[A2ACapabilities] = None):
        self.capabilities = capabilities or a2a_capabilities
        self.agent_orchestrator = agent_orchestrator
        self.is_initialized = False
    
    async def initialize(self) -> None:
        """Initialize the A2A handler"""
        try:
            self.is_initialized = True
            logger.info("A2A handler initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize A2A handler: {e}")
            raise
    
    async def handle_request(self, request: A2ARequest) -> A2AResponse:
        """Handle an A2A request"""
        start_time = datetime.utcnow()
        
        try:
            if not self.is_initialized:
                return self._create_error_response(
                    request,
                    "A2A handler not initialized",
                    0
                )
            
            # Validate capability exists
            if not self.capabilities.has_capability(request.capability_id):
                return self._create_error_response(
                    request,
                    f"Capability '{request.capability_id}' not found",
                    0
                )
            
            # Validate input parameters
            validation_error = self.capabilities.validate_capability_input(
                request.capability_id,
                request.parameters
            )
            if validation_error:
                return self._create_error_response(
                    request,
                    f"Parameter validation failed: {validation_error}",
                    0
                )
            
            # Route to appropriate handler
            result = await self._route_capability_request(request)
            
            # Calculate processing time
            processing_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Log the request
            await self._log_a2a_request(request, result, processing_time_ms)
            
            # Create response
            response = A2AResponse(
                request_id=request.message_id,
                sender_agent_id=self.capabilities.agent_id,
                receiver_agent_id=request.sender_agent_id,
                conversation_id=request.conversation_id,
                success=True,
                result=result,
                processing_time_ms=processing_time_ms
            )
            
            return response
            
        except Exception as e:
            processing_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            logger.error(f"A2A request handling failed: {e}")
            
            # Log the error
            await logging_service.log_error(e, {
                'context': 'a2a_request',
                'capability_id': request.capability_id,
                'parameters': request.parameters,
                'processing_time_ms': processing_time_ms
            })
            
            return self._create_error_response(
                request,
                f"Request handling failed: {str(e)}",
                processing_time_ms
            )
    
    async def _route_capability_request(self, request: A2ARequest) -> Dict[str, Any]:
        """Route request to appropriate capability handler"""
        capability_id = request.capability_id
        parameters = request.parameters
        
        if capability_id == "nasdaq.analyze_stock":
            return await self._handle_analyze_stock(parameters)
        elif capability_id == "nasdaq.get_market_data":
            return await self._handle_get_market_data(parameters)
        elif capability_id == "nasdaq.resolve_company_name":
            return await self._handle_resolve_company_name(parameters)
        elif capability_id == "nasdaq.query":
            return await self._handle_query(parameters)
        else:
            raise ValueError(f"No handler for capability: {capability_id}")
    
    async def _handle_analyze_stock(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle analyze_stock capability"""
        company_name_or_ticker = parameters.get("company_name_or_ticker", "")
        
        # Use the Langchain agent
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(
            f"Analyze {company_name_or_ticker} stock and provide investment recommendations"
        )
        
        if agent_result.get('success', False):
            return {
                'ticker': agent_result.get('ticker', 'unknown'),
                'company_name': agent_result.get('company_name', 'unknown'),
                'recommendation': agent_result.get('recommendation', 'Hold'),
                'confidence_score': agent_result.get('confidence_score', 50.0),
                'current_price': agent_result.get('current_price', 0.0),
                'price_change_percentage': agent_result.get('price_change_percentage', 0.0),
                'reasoning': agent_result.get('response', ''),
                'analysis_id': agent_result.get('extracted_data', {}).get('investment_analysis', {}).get('analysis_id', 'unknown'),
                'timestamp': agent_result.get('timestamp', datetime.utcnow().isoformat())
            }
        else:
            raise Exception(agent_result.get('error', 'Analysis failed'))
    
    async def _handle_get_market_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_market_data capability"""
        ticker = parameters.get("ticker", "")
        include_historical = parameters.get("include_historical", True)
        
        query = f"Get market data for {ticker}"
        if include_historical:
            query += " including 6-month historical data"
        
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(query)
        
        if agent_result.get('success', False):
            extracted_data = agent_result.get('extracted_data', {})
            market_data = extracted_data.get('market_data', {})
            
            if market_data:
                return market_data
            else:
                return {
                    'ticker': ticker,
                    'current_price': agent_result.get('current_price', 0.0),
                    'price_change_percentage': agent_result.get('price_change_percentage', 0.0),
                    'timestamp': datetime.utcnow().isoformat()
                }
        else:
            raise Exception(agent_result.get('error', f'Failed to retrieve market data for {ticker}'))
    
    async def _handle_resolve_company_name(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resolve_company_name capability"""
        company_name = parameters.get("company_name", "")
        
        query = f"What is the ticker symbol for {company_name}?"
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(query)
        
        if agent_result.get('success', False):
            extracted_data = agent_result.get('extracted_data', {})
            company_resolution = extracted_data.get('company_resolution', {})
            
            if company_resolution:
                return {
                    'input_name': company_name,
                    'ticker': company_resolution.get('ticker', 'unknown'),
                    'resolved_company_name': company_resolution.get('company_name', company_name),
                    'confidence': company_resolution.get('confidence', 1.0)
                }
            else:
                ticker = agent_result.get('ticker', 'unknown')
                return {
                    'input_name': company_name,
                    'ticker': ticker,
                    'resolved_company_name': agent_result.get('company_name', company_name),
                    'confidence': 0.8 if ticker != 'unknown' else 0.0
                }
        else:
            raise Exception(agent_result.get('error', f'Failed to resolve company name: {company_name}'))
    
    async def _handle_query(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle natural language query capability"""
        query = parameters.get("query", "")
        
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(query)
        
        if agent_result.get('success', False):
            return {
                'response': agent_result.get('response', ''),
                'ticker': agent_result.get('ticker', 'unknown'),
                'recommendation': agent_result.get('recommendation', 'Hold'),
                'confidence_score': agent_result.get('confidence_score', 50.0),
                'timestamp': agent_result.get('timestamp', datetime.utcnow().isoformat())
            }
        else:
            raise Exception(agent_result.get('error', 'Query processing failed'))
    
    async def _log_a2a_request(self, request: A2ARequest, result: Dict[str, Any], 
                               processing_time_ms: int) -> None:
        """Log A2A request to audit trail"""
        try:
            a2a_log_context = {
                'log_type': 'a2a_request',
                'capability_id': request.capability_id,
                'parameters': request.parameters,
                'sender_agent_id': request.sender_agent_id,
                'conversation_id': request.conversation_id,
                'result_keys': list(result.keys()),
                'processing_time_ms': processing_time_ms,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Log as API request for consistency
            await logging_service.log_api_request(
                endpoint=f"a2a://{request.capability_id}",
                method="A2A_REQUEST",
                request_data=request.parameters,
                response_data=result,
                status_code=200,
                processing_time_ms=processing_time_ms
            )
            
        except Exception as e:
            logger.error(f"Failed to log A2A request: {e}")
    
    def _create_error_response(self, request: A2ARequest, error_message: str, 
                               processing_time_ms: int) -> A2AResponse:
        """Create an error response"""
        return A2AResponse(
            request_id=request.message_id,
            sender_agent_id=self.capabilities.agent_id,
            receiver_agent_id=request.sender_agent_id,
            conversation_id=request.conversation_id,
            success=False,
            result={},
            error=error_message,
            processing_time_ms=processing_time_ms
        )
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            self.is_initialized = False
            logger.info("A2A handler cleaned up")
        except Exception as e:
            logger.error(f"A2A handler cleanup failed: {e}")
    
    def get_handler_status(self) -> Dict[str, Any]:
        """Get handler status"""
        return {
            'service': 'A2AHandler',
            'is_initialized': self.is_initialized,
            'agent_id': self.capabilities.agent_id,
            'capabilities_count': len(self.capabilities.get_all_capabilities()),
            'timestamp': datetime.utcnow().isoformat()
        }


# Global A2A handler instance
a2a_handler = A2AHandler()