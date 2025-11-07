"""
MongoDB database connection and utilities for NASDAQ Stock Agent
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import IndexModel, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
from src.config.settings import settings
from src.models.logging import AnalysisLogEntry, ErrorLogEntry

logger = logging.getLogger(__name__)


class MongoDBClient:
    """MongoDB client with connection management and schema setup"""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
        self._collections: Dict[str, AsyncIOMotorCollection] = {}
        
    async def connect(self) -> None:
        """Establish connection to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(
                settings.mongodb_url,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test the connection
            await self.client.admin.command('ping')
            
            self.database = self.client[settings.mongodb_database]
            
            # Initialize collections
            await self._setup_collections()
            await self._create_indexes()
            
            logger.info(f"Connected to MongoDB: {settings.mongodb_database}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _setup_collections(self) -> None:
        """Initialize MongoDB collections"""
        collection_names = [
            "analyses",      # Stock analysis logs
            "errors",        # Error logs
            "agent_registry" # Agent fact cards
        ]
        
        for collection_name in collection_names:
            self._collections[collection_name] = self.database[collection_name]
    
    async def _create_indexes(self) -> None:
        """Create indexes for optimal query performance and TTL"""
        try:
            # Analyses collection indexes
            analyses_indexes = [
                IndexModel([("analysis_id", ASCENDING)], unique=True),
                IndexModel([("ticker_symbol", ASCENDING)]),
                IndexModel([("timestamp", DESCENDING)]),
                IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0)  # TTL index
            ]
            await self._collections["analyses"].create_indexes(analyses_indexes)
            
            # Errors collection indexes
            errors_indexes = [
                IndexModel([("error_id", ASCENDING)], unique=True),
                IndexModel([("error_type", ASCENDING)]),
                IndexModel([("timestamp", DESCENDING)]),
                IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0)  # TTL index
            ]
            await self._collections["errors"].create_indexes(errors_indexes)
            
            # Agent registry collection indexes
            agent_indexes = [
                IndexModel([("agent_id", ASCENDING)], unique=True),
                IndexModel([("agent_domain", ASCENDING)]),
                IndexModel([("agent_specialization", ASCENDING)])
            ]
            await self._collections["agent_registry"].create_indexes(agent_indexes)
            
            logger.info("MongoDB indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create MongoDB indexes: {e}")
            raise
    
    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Get a MongoDB collection"""
        if collection_name not in self._collections:
            raise ValueError(f"Collection '{collection_name}' not found")
        return self._collections[collection_name]
    
    async def health_check(self) -> Dict[str, Any]:
        """Check MongoDB connection health"""
        try:
            if not self.client:
                return {"status": "disconnected", "error": "No client connection"}
            
            # Ping the database
            await self.client.admin.command('ping')
            
            # Get database stats
            stats = await self.database.command("dbStats")
            
            return {
                "status": "healthy",
                "database": settings.mongodb_database,
                "collections": len(self._collections),
                "data_size": stats.get("dataSize", 0),
                "storage_size": stats.get("storageSize", 0)
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def cleanup_expired_entries(self) -> Dict[str, int]:
        """Manual cleanup of expired entries (TTL should handle this automatically)"""
        try:
            current_time = datetime.utcnow()
            
            # Count and delete expired analyses
            analyses_deleted = await self._collections["analyses"].delete_many({
                "expires_at": {"$lt": current_time}
            })
            
            # Count and delete expired errors
            errors_deleted = await self._collections["errors"].delete_many({
                "expires_at": {"$lt": current_time}
            })
            
            cleanup_result = {
                "analyses_deleted": analyses_deleted.deleted_count,
                "errors_deleted": errors_deleted.deleted_count,
                "cleanup_timestamp": current_time
            }
            
            logger.info(f"Cleanup completed: {cleanup_result}")
            return cleanup_result
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            raise


class DatabaseService:
    """High-level database service for application operations"""
    
    def __init__(self, mongodb_client: MongoDBClient):
        self.mongodb_client = mongodb_client
    
    async def log_analysis(self, log_entry: AnalysisLogEntry) -> str:
        """Store analysis log entry in MongoDB"""
        try:
            collection = self.mongodb_client.get_collection("analyses")
            result = await collection.insert_one(log_entry.to_dict())
            
            logger.info(f"Analysis logged: {log_entry.analysis_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Failed to log analysis: {e}")
            raise
    
    async def log_error(self, error_entry: ErrorLogEntry) -> str:
        """Store error log entry in MongoDB"""
        try:
            collection = self.mongodb_client.get_collection("errors")
            result = await collection.insert_one(error_entry.to_dict())
            
            logger.error(f"Error logged: {error_entry.error_id} - {error_entry.error_message}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Failed to log error: {e}")
            raise
    
    async def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve analysis by ID"""
        try:
            collection = self.mongodb_client.get_collection("analyses")
            result = await collection.find_one({"analysis_id": analysis_id})
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve analysis {analysis_id}: {e}")
            raise
    
    async def get_analyses_by_ticker(self, ticker: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recent analyses for a ticker symbol"""
        try:
            collection = self.mongodb_client.get_collection("analyses")
            cursor = collection.find(
                {"ticker_symbol": ticker.upper()}
            ).sort("timestamp", DESCENDING).limit(limit)
            
            results = []
            async for document in cursor:
                results.append(document)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to retrieve analyses for {ticker}: {e}")
            raise
    
    async def get_recent_analyses(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recent analyses across all stocks"""
        try:
            collection = self.mongodb_client.get_collection("analyses")
            cursor = collection.find().sort("timestamp", DESCENDING).limit(limit)
            
            results = []
            async for document in cursor:
                results.append(document)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to retrieve recent analyses: {e}")
            raise
    
    async def store_agent_fact_card(self, agent_data: Dict[str, Any]) -> str:
        """Store or update agent fact card in registry"""
        try:
            collection = self.mongodb_client.get_collection("agent_registry")
            
            # Upsert the agent fact card
            result = await collection.replace_one(
                {"agent_id": agent_data["agent_id"]},
                agent_data,
                upsert=True
            )
            
            logger.info(f"Agent fact card stored: {agent_data['agent_id']}")
            return agent_data["agent_id"]
            
        except Exception as e:
            logger.error(f"Failed to store agent fact card: {e}")
            raise
    
    async def get_agent_fact_card(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve agent fact card by ID"""
        try:
            collection = self.mongodb_client.get_collection("agent_registry")
            result = await collection.find_one({"agent_id": agent_id})
            return result
            
        except Exception as e:
            logger.error(f"Failed to retrieve agent fact card {agent_id}: {e}")
            raise


# Global MongoDB client instance
mongodb_client = MongoDBClient()
database_service = DatabaseService(mongodb_client)