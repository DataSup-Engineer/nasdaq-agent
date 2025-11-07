"""
Database initialization and schema setup for NASDAQ Stock Agent
"""
import asyncio
import logging
from datetime import datetime
from src.services.database import mongodb_client, database_service
from src.models.analysis import AgentFactCard

logger = logging.getLogger(__name__)


async def initialize_database():
    """Initialize MongoDB database with schema and default data"""
    try:
        # Connect to MongoDB
        await mongodb_client.connect()
        
        # Create default agent fact card
        await create_default_agent_fact_card()
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def create_default_agent_fact_card():
    """Create the default NASDAQ Stock Agent fact card"""
    try:
        agent_fact_card = AgentFactCard(
            agent_id="nasdaq-stock-agent-v1",
            agent_name="NASDAQ Stock Agent",
            agent_domain="Financial Analysis",
            agent_specialization="NASDAQ Stock Analysis and Investment Recommendations",
            agent_description="AI-powered agent that provides comprehensive stock analysis and investment recommendations for NASDAQ-listed securities using real-time market data and advanced AI analysis.",
            agent_capabilities=[
                "Natural language stock query processing",
                "Real-time NASDAQ market data retrieval",
                "6-month historical trend analysis",
                "AI-powered investment recommendations (Buy/Hold/Sell)",
                "Risk assessment and confidence scoring",
                "Company name to ticker symbol resolution",
                "Comprehensive logging and audit trails"
            ],
            registry_url="mongodb://localhost:27017/nasdaq_stock_agent/agent_registry",
            public_url="http://localhost:8000/api/v1"
        )
        
        # Convert to dictionary for storage
        agent_data = {
            "agent_id": agent_fact_card.agent_id,
            "agent_name": agent_fact_card.agent_name,
            "agent_domain": agent_fact_card.agent_domain,
            "agent_specialization": agent_fact_card.agent_specialization,
            "agent_description": agent_fact_card.agent_description,
            "agent_capabilities": agent_fact_card.agent_capabilities,
            "registry_url": agent_fact_card.registry_url,
            "public_url": agent_fact_card.public_url,
            "created_at": agent_fact_card.created_at,
            "updated_at": agent_fact_card.updated_at
        }
        
        # Store in database
        await database_service.store_agent_fact_card(agent_data)
        
        logger.info("Default agent fact card created successfully")
        
    except Exception as e:
        logger.error(f"Failed to create default agent fact card: {e}")
        raise


async def verify_database_setup():
    """Verify that database setup is correct"""
    try:
        # Check MongoDB health
        health_status = await mongodb_client.health_check()
        
        if health_status["status"] != "healthy":
            raise Exception(f"Database health check failed: {health_status}")
        
        # Verify agent fact card exists
        agent_card = await database_service.get_agent_fact_card("nasdaq-stock-agent-v1")
        
        if not agent_card:
            raise Exception("Default agent fact card not found")
        
        logger.info("Database setup verification completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database setup verification failed: {e}")
        return False


if __name__ == "__main__":
    # Run database initialization
    asyncio.run(initialize_database())