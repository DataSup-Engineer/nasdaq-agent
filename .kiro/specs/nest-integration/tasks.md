# NEST Integration Implementation Plan

- [x] 1. Set up NEST integration structure
  - Create `src/nest/` directory for NEST components
  - Install python-a2a dependency
  - _Requirements: 1.1, 8.5_

- [x] 2. Implement NEST configuration
- [x] 2.1 Create NESTConfig class
  - Implement configuration loading from environment variables
  - Add validation methods for required fields
  - Implement should_enable_nest() logic
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 2.2 Add NEST environment variables to .env.example
  - Document all NEST configuration options
  - Provide example values
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 3. Implement agent logic adapter
- [x] 3.1 Create agent_logic.py module
  - Implement process_a2a_message() function
  - Add stock query parsing logic
  - Add command handling (/help, /status, /ping)
  - Format analysis results for A2A responses
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 3.2 Integrate with existing services
  - Connect to enhanced_nlp_service for ticker resolution
  - Connect to comprehensive_analysis_service for analysis
  - Reuse existing service instances
  - _Requirements: 4.2_

- [x] 4. Implement agent bridge
- [x] 4.1 Create StockAgentBridge class
  - Extend A2AServer from python_a2a
  - Implement handle_message() method
  - Add message routing logic
  - _Requirements: 4.1, 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 4.2 Implement stock query handling
  - Create _handle_stock_query() method
  - Call agent_logic.process_a2a_message()
  - Format responses as Message objects
  - _Requirements: 4.1, 4.2, 4.3_

- [x] 4.3 Implement A2A forwarding
  - Create _handle_agent_message() method for @agent-id syntax
  - Implement _lookup_agent() for registry queries
  - Add A2AClient integration for forwarding messages
  - Handle agent not found errors
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 4.4 Implement command handling
  - Create _handle_command() method
  - Support /help, /status, /ping commands
  - Return formatted command responses
  - _Requirements: 3.4_

- [x] 4.5 Implement response creation
  - Create _create_response() helper method
  - Format messages with [nasdaq-stock-agent] prefix
  - Include parent_message_id and conversation_id
  - _Requirements: 10.2, 10.3, 10.4, 10.5_

- [x] 5. Implement NEST adapter
- [x] 5.1 Create NESTAdapter class
  - Initialize with NESTConfig
  - Create StockAgentBridge instance
  - Set up server lifecycle management
  - _Requirements: 1.1, 1.3_

- [x] 5.2 Implement server startup
  - Create start_async() method
  - Start A2A server in background thread
  - Handle initialization errors gracefully
  - _Requirements: 1.1, 8.1_

- [x] 5.3 Implement registry registration
  - Create _register() method with retry logic
  - POST to {registry_url}/register endpoint
  - Include agent_id, agent_url, api_url, agent_facts_url
  - Implement exponential backoff for retries
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 8.2_

- [x] 5.4 Implement server shutdown
  - Create stop_async() method
  - Deregister from NANDA Registry
  - Stop A2A server thread gracefully
  - Clean up resources
  - _Requirements: 2.5_

- [x] 5.5 Implement status monitoring
  - Create get_status() method
  - Return server status, registration status
  - Implement is_running() check
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 6. Integrate NEST with main application
- [x] 6.1 Modify main.py for NEST initialization
  - Add global _nest_adapter variable
  - Create initialize_nest() function
  - Create shutdown_nest() function
  - _Requirements: 1.1, 6.1, 6.2_

- [x] 6.2 Update FastAPI lifespan
  - Call initialize_nest() on startup
  - Call shutdown_nest() on shutdown
  - Handle NEST failures gracefully
  - _Requirements: 1.1, 8.1_

- [x] 6.3 Add NEST status to health checks
  - Update health endpoint to include NEST status
  - Report nest_enabled, nest_status, registry_status
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 7. Enhance agent facts endpoint
- [x] 7.1 Update /api/v1/agent/info endpoint
  - Add NEST-specific metadata
  - Include a2a_endpoint when NEST is enabled
  - Add supported_operations list
  - Include agent_domain and agent_specialization
  - _Requirements: 3.1, 3.2, 3.3_

- [x] 7.2 Add A2A info command support
  - Handle /info command in agent bridge
  - Return agent facts via A2A
  - _Requirements: 3.4_

- [x] 8. Implement logging for NEST operations
- [x] 8.1 Add A2A message logging
  - Log incoming A2A messages with conversation_id
  - Log outgoing A2A messages to other agents
  - Include message content summaries
  - _Requirements: 7.1, 7.2_

- [x] 8.2 Add NEST lifecycle logging
  - Log NEST initialization success/failure
  - Log registry registration status
  - Log server startup/shutdown
  - _Requirements: 7.3_

- [x] 8.3 Add error logging
  - Log A2A processing errors with stack traces
  - Log registry connection failures
  - Log agent lookup failures
  - _Requirements: 7.4_

- [x] 8.4 Add performance logging
  - Log A2A message processing time
  - Track A2A request count
  - _Requirements: 7.5_

- [x] 9. Update dependencies and configuration
- [x] 9.1 Update requirements.txt
  - Add python-a2a dependency
  - Add requests dependency (if not present)
  - _Requirements: 8.5_

- [x] 9.2 Update .env file
  - Add NEST configuration variables
  - Set NEST_ENABLED=false by default
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 9.3 Update README.md
  - Document NEST integration
  - Add A2A usage examples
  - Document environment variables
  - _Requirements: All_

- [ ] 10. Testing and validation
- [ ] 10.1 Test NEST configuration
  - Test configuration loading
  - Test validation logic
  - Test enable/disable functionality
  - _Requirements: 6.1, 6.2_

- [ ] 10.2 Test A2A message handling
  - Test stock query processing
  - Test command handling
  - Test error responses
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 10.3 Test registry integration
  - Test registration with NANDA Registry
  - Test agent lookup
  - Test deregistration
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 10.4 Test dual interface operation
  - Start both FastAPI and NEST servers
  - Send concurrent REST and A2A requests
  - Verify both work without interference
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [ ] 10.5 Test error handling
  - Test NEST initialization failure
  - Test registry connection failure
  - Test A2A message processing errors
  - Verify REST API continues working
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 10.6 Test agent-to-agent communication
  - Test @agent-id message forwarding
  - Test agent lookup in registry
  - Test error handling for missing agents
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
