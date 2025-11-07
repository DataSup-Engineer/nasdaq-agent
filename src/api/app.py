"""
FastAPI application factory and configuration
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from src.config.settings import settings
from src.api.routers import analysis, health, agent
from src.services.logging_middleware import RequestLoggingMiddleware, monitoring_service
from src.services.database import mongodb_client
from src.services.db_init import initialize_database
from src.services.cache_service import global_cache
from src.api.middleware.validation import ValidationMiddleware
from src.api.error_handlers import setup_error_handlers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting NASDAQ Stock Agent...")
    
    try:
        # Initialize database
        await initialize_database()
        # Start global in-memory cache background task
        try:
            await global_cache.start()
        except Exception as e:
            logger.warning(f"Failed to start global cache background task: {e}")
        
        # Initialize monitoring
        await monitoring_service.initialize_monitoring()
        
        logger.info("NASDAQ Stock Agent started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down NASDAQ Stock Agent...")
    
    try:
        # Disconnect from database
        await mongodb_client.disconnect()
        # Shutdown global cache
        try:
            await global_cache.shutdown()
        except Exception as e:
            logger.warning(f"Failed to shutdown global cache cleanly: {e}")
        
        logger.info("NASDAQ Stock Agent shut down successfully")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        AI-powered NASDAQ stock analysis and investment recommendations using Langchain, 
        Anthropic Claude, and real-time market data.
        
        ## Features
        
        * **Natural Language Processing**: Query stocks using company names or natural language
        * **Real-time Market Data**: Current prices, volume, and 6-month historical data
        * **AI-Powered Analysis**: Investment recommendations with confidence scores
        * **Comprehensive Logging**: Full audit trails and performance monitoring
        * **Agent Registry**: Discoverable agent capabilities and information
        
        ## Example Queries
        
        * "What do you think about Apple stock?"
        * "Should I buy Tesla?"
        * "Analyze Microsoft"
        * "AAPL"
        
        ## Response Format
        
        All analysis responses include:
        * Investment recommendation (Buy/Hold/Sell)
        * Confidence score (0-100)
        * Current price and market data
        * Detailed reasoning and key factors
        * Risk assessment
        """,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add middleware
    app.add_middleware(ValidationMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Include routers
    app.include_router(analysis.router)
    app.include_router(health.router)
    app.include_router(agent.router)
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for unhandled errors"""
        logger.error(f"Unhandled exception in {request.method} {request.url}: {exc}")
        
        return JSONResponse(
            status_code=500,
            content={
                "error_code": "INTERNAL_SERVER_ERROR",
                "error_message": "An internal server error occurred",
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        )
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint with API information"""
        return {
            "service": settings.app_name,
            "version": settings.app_version,
            "description": "AI-powered NASDAQ stock analysis and investment recommendations",
            "documentation": "/docs",
            "health_check": "/health",
            "api_endpoints": {
                "analyze_stock": "/api/v1/analyze",
                "agent_info": "/api/v1/agent/info",
                "system_status": "/status"
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    
    return app