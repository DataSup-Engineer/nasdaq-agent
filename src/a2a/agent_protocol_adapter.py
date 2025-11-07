"""
Agent Protocol adapter for NASDAQ Stock Agent
Integrates with the official agent-protocol package
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Initialize logger before using it
logger = logging.getLogger(__name__)

try:
    from agent_protocol import Agent, Task, Step, StepResult, TaskResult
    AGENT_PROTOCOL_AVAILABLE = True
    logger.info("agent-protocol package is available")
except ImportError:
    AGENT_PROTOCOL_AVAILABLE = False
    logger.info("agent-protocol package not installed (optional)")
    # Fallback types for when package is not installed
    Agent = None
    Task = None
    Step = None
    StepResult = None
    TaskResult = None

from agents.stock_analysis_agent import agent_orchestrator


class NASDAQStockAgent:
    """NASDAQ Stock Agent implementation using agent-protocol"""
    
    def __init__(self):
        self.agent_orchestrator = agent_orchestrator
        self.agent_id = "nasdaq-stock-agent"
        self.agent_name = "NASDAQ Stock Agent"
        self.agent_description = "AI-powered NASDAQ stock analysis and investment recommendations"
        self.version = "1.0.0"
    
    async def execute_task(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task using the agent protocol
        
        Args:
            task_input: Task input containing action and parameters
            
        Returns:
            Task result with output data
        """
        try:
            action = task_input.get('action', 'analyze')
            parameters = task_input.get('parameters', {})
            
            if action == 'analyze_stock':
                return await self._analyze_stock(parameters)
            elif action == 'get_market_data':
                return await self._get_market_data(parameters)
            elif action == 'resolve_company_name':
                return await self._resolve_company_name(parameters)
            elif action == 'query':
                return await self._process_query(parameters)
            else:
                return {
                    'success': False,
                    'error': f"Unknown action: {action}",
                    'available_actions': [
                        'analyze_stock',
                        'get_market_data',
                        'resolve_company_name',
                        'query'
                    ]
                }
                
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _analyze_stock(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a stock"""
        company_name_or_ticker = parameters.get('company_name_or_ticker', '')
        
        if not company_name_or_ticker:
            return {
                'success': False,
                'error': 'Missing required parameter: company_name_or_ticker'
            }
        
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(
            f"Analyze {company_name_or_ticker} stock and provide investment recommendations"
        )
        
        if agent_result.get('success', False):
            return {
                'success': True,
                'output': {
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
            }
        else:
            return {
                'success': False,
                'error': agent_result.get('error', 'Analysis failed')
            }
    
    async def _get_market_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get market data for a stock"""
        ticker = parameters.get('ticker', '')
        include_historical = parameters.get('include_historical', True)
        
        if not ticker:
            return {
                'success': False,
                'error': 'Missing required parameter: ticker'
            }
        
        query = f"Get market data for {ticker}"
        if include_historical:
            query += " including 6-month historical data"
        
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(query)
        
        if agent_result.get('success', False):
            extracted_data = agent_result.get('extracted_data', {})
            market_data = extracted_data.get('market_data', {})
            
            return {
                'success': True,
                'output': market_data if market_data else {
                    'ticker': ticker,
                    'current_price': agent_result.get('current_price', 0.0),
                    'price_change_percentage': agent_result.get('price_change_percentage', 0.0),
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
        else:
            return {
                'success': False,
                'error': agent_result.get('error', f'Failed to retrieve market data for {ticker}')
            }
    
    async def _resolve_company_name(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve company name to ticker"""
        company_name = parameters.get('company_name', '')
        
        if not company_name:
            return {
                'success': False,
                'error': 'Missing required parameter: company_name'
            }
        
        query = f"What is the ticker symbol for {company_name}?"
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(query)
        
        if agent_result.get('success', False):
            extracted_data = agent_result.get('extracted_data', {})
            company_resolution = extracted_data.get('company_resolution', {})
            
            if company_resolution:
                output = {
                    'input_name': company_name,
                    'ticker': company_resolution.get('ticker', 'unknown'),
                    'resolved_company_name': company_resolution.get('company_name', company_name),
                    'confidence': company_resolution.get('confidence', 1.0)
                }
            else:
                ticker = agent_result.get('ticker', 'unknown')
                output = {
                    'input_name': company_name,
                    'ticker': ticker,
                    'resolved_company_name': agent_result.get('company_name', company_name),
                    'confidence': 0.8 if ticker != 'unknown' else 0.0
                }
            
            return {
                'success': True,
                'output': output
            }
        else:
            return {
                'success': False,
                'error': agent_result.get('error', f'Failed to resolve company name: {company_name}')
            }
    
    async def _process_query(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process natural language query"""
        query = parameters.get('query', '')
        
        if not query:
            return {
                'success': False,
                'error': 'Missing required parameter: query'
            }
        
        agent_result = await self.agent_orchestrator.stock_agent.analyze_stock_query(query)
        
        if agent_result.get('success', False):
            return {
                'success': True,
                'output': {
                    'response': agent_result.get('response', ''),
                    'ticker': agent_result.get('ticker', 'unknown'),
                    'recommendation': agent_result.get('recommendation', 'Hold'),
                    'confidence_score': agent_result.get('confidence_score', 50.0),
                    'timestamp': agent_result.get('timestamp', datetime.utcnow().isoformat())
                }
            }
        else:
            return {
                'success': False,
                'error': agent_result.get('error', 'Query processing failed')
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            'agent_id': self.agent_id,
            'name': self.agent_name,
            'description': self.agent_description,
            'version': self.version,
            'protocol': 'agent-protocol',
            'capabilities': [
                {
                    'action': 'analyze_stock',
                    'description': 'Analyze a NASDAQ stock and provide investment recommendations',
                    'parameters': {
                        'company_name_or_ticker': 'Company name or ticker symbol'
                    }
                },
                {
                    'action': 'get_market_data',
                    'description': 'Retrieve current and historical market data',
                    'parameters': {
                        'ticker': 'Stock ticker symbol',
                        'include_historical': 'Include 6-month historical data (optional)'
                    }
                },
                {
                    'action': 'resolve_company_name',
                    'description': 'Convert company name to ticker symbol',
                    'parameters': {
                        'company_name': 'Company name to resolve'
                    }
                },
                {
                    'action': 'query',
                    'description': 'Process natural language query about stocks',
                    'parameters': {
                        'query': 'Natural language query'
                    }
                }
            ],
            'timestamp': datetime.utcnow().isoformat()
        }


# Global agent instance
nasdaq_agent = NASDAQStockAgent()


def create_agent_protocol_server():
    """
    Create an agent-protocol server instance
    
    Returns:
        Agent server instance if agent-protocol is available, None otherwise
    """
    if not AGENT_PROTOCOL_AVAILABLE:
        logger.warning("agent-protocol package not available")
        return None
    
    try:
        # Create agent with the official agent-protocol package
        agent = Agent(
            name=nasdaq_agent.agent_name,
            description=nasdaq_agent.agent_description
        )
        
        @agent.task()
        async def execute_stock_task(task_input: str) -> str:
            """Execute a stock analysis task"""
            import json
            
            # Parse task input
            try:
                task_data = json.loads(task_input) if isinstance(task_input, str) else task_input
            except json.JSONDecodeError:
                # Treat as natural language query
                task_data = {'action': 'query', 'parameters': {'query': task_input}}
            
            # Execute task
            result = await nasdaq_agent.execute_task(task_data)
            
            # Return result as JSON string
            return json.dumps(result, default=str)
        
        logger.info("Agent protocol server created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create agent protocol server: {e}")
        return None