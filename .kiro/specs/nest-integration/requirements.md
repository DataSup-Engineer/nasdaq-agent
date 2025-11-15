# NEST Integration Requirements

## Introduction

This document outlines the requirements for integrating the NASDAQ Stock Agent with the NANDA NEST (Network of Autonomous Distributed Agents) framework. The integration will enable agent-to-agent (A2A) communication while maintaining the existing FastAPI REST interface.

## Glossary

- **NEST**: NANDA Sandbox and Testbed - Framework for deploying and managing specialized AI agents
- **A2A Protocol**: Agent-to-Agent communication protocol using python_a2a library
- **NANDA Registry**: Central registry service for agent discovery at http://registry.chat39.com:6900
- **Agent Facts**: Metadata about agent capabilities, domain, and specialization
- **NASDAQ Stock Agent**: The AI-powered stock analysis agent being integrated
- **FastAPI Application**: Existing REST API server running on port 8000
- **NEST Adapter**: Bridge component that translates A2A messages to agent logic

## Requirements

### Requirement 1: Dual Interface Support

**User Story:** As a system architect, I want the agent to support both REST API and A2A protocols, so that existing integrations continue working while enabling NEST communication.

#### Acceptance Criteria

1. WHEN the agent starts, THE NASDAQ Stock Agent SHALL initialize both FastAPI server on port 8000 and NEST A2A server on port 6000
2. WHEN a REST API request arrives at port 8000, THE NASDAQ Stock Agent SHALL process it through the existing FastAPI handlers
3. WHEN an A2A message arrives at port 6000, THE NASDAQ Stock Agent SHALL process it through the NEST adapter
4. WHEN both servers are running, THE NASDAQ Stock Agent SHALL handle requests concurrently without interference

### Requirement 2: NEST Registry Registration

**User Story:** As an agent operator, I want the agent to automatically register with NANDA Registry, so that other agents can discover and communicate with it.

#### Acceptance Criteria

1. WHEN the agent starts with NEST enabled, THE NASDAQ Stock Agent SHALL register with the NANDA Registry at the configured registry URL
2. WHEN registering, THE NASDAQ Stock Agent SHALL provide agent_id as "nasdaq-stock-agent" and agent_url as the public A2A endpoint
3. WHEN registration succeeds, THE NASDAQ Stock Agent SHALL log confirmation with HTTP 200 status
4. WHEN registration fails, THE NASDAQ Stock Agent SHALL log warning and continue operation in standalone mode
5. WHEN the agent shuts down gracefully, THE NASDAQ Stock Agent SHALL deregister from the NANDA Registry

### Requirement 3: Agent Facts Endpoint

**User Story:** As another agent in the NEST network, I want to query the NASDAQ Stock Agent's capabilities, so that I know what services it provides.

#### Acceptance Criteria

1. WHEN an agent facts request arrives, THE NASDAQ Stock Agent SHALL return agent metadata including agent_id, agent_name, domain, specialization, description, and capabilities
2. WHEN returning agent facts, THE NASDAQ Stock Agent SHALL include the list of supported operations: stock analysis, ticker resolution, investment recommendations
3. WHEN agent facts are requested via REST, THE NASDAQ Stock Agent SHALL serve them at GET /api/v1/agent/info
4. WHEN agent facts are requested via A2A, THE NASDAQ Stock Agent SHALL respond to "/help" or "/info" commands

### Requirement 4: A2A Message Handling

**User Story:** As another NEST agent, I want to send stock analysis requests to the NASDAQ Stock Agent using A2A protocol, so that I can get investment recommendations for my users.

#### Acceptance Criteria

1. WHEN an A2A message with stock query arrives, THE NASDAQ Stock Agent SHALL parse the message content and extract the stock symbol or company name
2. WHEN processing A2A stock queries, THE NASDAQ Stock Agent SHALL use the existing comprehensive_analysis_service to generate analysis
3. WHEN analysis completes, THE NASDAQ Stock Agent SHALL format the response as A2A Message with TextContent
4. WHEN analysis fails, THE NASDAQ Stock Agent SHALL return an error message in A2A format with details
5. WHEN A2A message format is invalid, THE NASDAQ Stock Agent SHALL return helpful error message explaining expected format

### Requirement 5: Agent-to-Agent Communication

**User Story:** As the NASDAQ Stock Agent, I want to communicate with other agents using @agent-id syntax, so that I can forward requests or collaborate on complex queries.

#### Acceptance Criteria

1. WHEN a message starts with "@agent-id", THE NASDAQ Stock Agent SHALL look up the target agent in NANDA Registry
2. WHEN target agent is found, THE NASDAQ Stock Agent SHALL send the message using A2A protocol
3. WHEN target agent responds, THE NASDAQ Stock Agent SHALL return the response to the original requester
4. WHEN target agent is not found, THE NASDAQ Stock Agent SHALL return error message "Agent {agent-id} not found"
5. WHEN registry lookup fails, THE NASDAQ Stock Agent SHALL log warning and return error to requester

### Requirement 6: Configuration Management

**User Story:** As a deployment engineer, I want to configure NEST integration via environment variables, so that I can enable/disable it without code changes.

#### Acceptance Criteria

1. WHEN NEST_ENABLED environment variable is set to "true", THE NASDAQ Stock Agent SHALL initialize NEST adapter
2. WHEN NEST_ENABLED is "false" or unset, THE NASDAQ Stock Agent SHALL run in REST-only mode
3. WHEN NEST_PORT is configured, THE NASDAQ Stock Agent SHALL use that port for A2A server
4. WHEN NEST_REGISTRY_URL is configured, THE NASDAQ Stock Agent SHALL use it for registration
5. WHEN NEST_PUBLIC_URL is configured, THE NASDAQ Stock Agent SHALL register with that URL

### Requirement 7: Logging and Monitoring

**User Story:** As a system administrator, I want comprehensive logging of A2A interactions, so that I can monitor and debug agent communication.

#### Acceptance Criteria

1. WHEN an A2A message is received, THE NASDAQ Stock Agent SHALL log the message with conversation_id, sender, and content summary
2. WHEN sending A2A messages to other agents, THE NASDAQ Stock Agent SHALL log the target agent and message summary
3. WHEN NEST registration occurs, THE NASDAQ Stock Agent SHALL log registration status and agent URL
4. WHEN A2A errors occur, THE NASDAQ Stock Agent SHALL log detailed error information including stack traces
5. WHEN A2A messages are processed, THE NASDAQ Stock Agent SHALL include processing time in logs

### Requirement 8: Error Handling and Resilience

**User Story:** As a reliability engineer, I want the agent to handle NEST failures gracefully, so that the core REST API remains available even if A2A communication fails.

#### Acceptance Criteria

1. WHEN NEST adapter initialization fails, THE NASDAQ Stock Agent SHALL log error and continue with REST-only mode
2. WHEN registry registration fails, THE NASDAQ Stock Agent SHALL retry up to 3 times with exponential backoff
3. WHEN A2A message processing fails, THE NASDAQ Stock Agent SHALL return error response without crashing
4. WHEN another agent is unreachable, THE NASDAQ Stock Agent SHALL timeout after 30 seconds and return error
5. WHEN python_a2a library is not installed, THE NASDAQ Stock Agent SHALL detect this and disable NEST features

### Requirement 9: Health Checks

**User Story:** As a monitoring system, I want to check if NEST integration is healthy, so that I can alert operators of issues.

#### Acceptance Criteria

1. WHEN health check endpoint is called, THE NASDAQ Stock Agent SHALL include NEST status in response
2. WHEN NEST is enabled and running, THE NASDAQ Stock Agent SHALL report nest_status as "healthy"
3. WHEN NEST is disabled, THE NASDAQ Stock Agent SHALL report nest_status as "disabled"
4. WHEN NEST has errors, THE NASDAQ Stock Agent SHALL report nest_status as "unhealthy" with error details
5. WHEN registry is unreachable, THE NASDAQ Stock Agent SHALL report registry_status as "unreachable"

### Requirement 10: Message Format Compatibility

**User Story:** As a NEST framework user, I want the NASDAQ Stock Agent to follow standard A2A message formats, so that it integrates seamlessly with other NEST agents.

#### Acceptance Criteria

1. WHEN receiving A2A messages, THE NASDAQ Stock Agent SHALL accept Message objects with role, content, and conversation_id
2. WHEN sending A2A responses, THE NASDAQ Stock Agent SHALL create Message objects with MessageRole.AGENT
3. WHEN including text content, THE NASDAQ Stock Agent SHALL use TextContent type
4. WHEN responding to messages, THE NASDAQ Stock Agent SHALL include parent_message_id linking to original message
5. WHEN creating responses, THE NASDAQ Stock Agent SHALL prefix responses with "[nasdaq-stock-agent]" identifier
