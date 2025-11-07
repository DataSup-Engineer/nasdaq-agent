#!/usr/bin/env python3
"""
Standalone Agent Protocol server for NASDAQ Stock Agent
Uses the official agent-protocol package
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.a2a.agent_protocol_adapter import (
    create_agent_protocol_server,
    AGENT_PROTOCOL_AVAILABLE,
    nasdaq_agent
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point for agent-protocol server"""
    
    if not AGENT_PROTOCOL_AVAILABLE:
        logger.error("agent-protocol package is not installed")
        logger.error("Install it with: pip install agent-protocol")
        sys.exit(1)
    
    try:
        logger.info("Starting NASDAQ Stock Agent with agent-protocol...")
        
        # Initialize core services
        logger.info("Initializing core services...")
        from src.services.database import mongodb_client
        await mongodb_client.connect()
        
        from src.services.logging_service import logging_service
        stats = await logging_service.get_logging_statistics()
        logger.info(f"Logging service initialized: {stats.get('service')}")
        
        from src.agents.stock_analysis_agent import agent_orchestrator
        health = await agent_orchestrator.get_health_status()
        logger.info(f"Agent orchestrator initialized: {health.get('overall_status')}")
        
        # Create agent-protocol server
        logger.info("Creating agent-protocol server...")
        agent = create_agent_protocol_server()
        
        if not agent:
            logger.error("Failed to create agent-protocol server")
            sys.exit(1)
        
        # Get agent info
        agent_info = nasdaq_agent.get_agent_info()
        logger.info(f"Agent: {agent_info['name']}")
        logger.info(f"Version: {agent_info['version']}")
        logger.info(f"Capabilities: {len(agent_info['capabilities'])}")
        
        # Start the agent server
        logger.info("Starting agent-protocol server on http://localhost:8001")
        logger.info("Agent is ready to receive tasks!")
        logger.info("Press Ctrl+C to stop")
        
        # Run the agent server
        await agent.start(port=8001)
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Agent protocol server failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup
        logger.info("Shutting down agent-protocol server...")
        try:
            from src.services.database import mongodb_client
            await mongodb_client.disconnect()
            
            from src.services.logging_service import logging_service
            logging_service.shutdown()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Agent protocol server stopped by user")
    except Exception as e:
        logger.error(f"Agent protocol server failed: {e}")
        sys.exit(1)