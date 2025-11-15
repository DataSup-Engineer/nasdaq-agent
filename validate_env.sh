#!/bin/bash

###############################################################################
# NASDAQ Stock Agent - Environment Validation Script
#
# This script validates that all required environment variables are set
# before starting the application.
#
# Exit codes:
#   0 - All required variables are valid
#   1 - One or more required variables are missing or invalid
#
# Usage:
#   ./validate_env.sh [path_to_env_file]
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default .env file location
ENV_FILE="${1:-/opt/nasdaq-agent/.env}"

# Validation status
VALIDATION_FAILED=0

# Required environment variables
REQUIRED_VARS=(
    "ANTHROPIC_API_KEY"
    "ANTHROPIC_MODEL"
    "HOST"
    "PORT"
)

# Optional but recommended variables
RECOMMENDED_VARS=(
    "APP_NAME"
    "APP_VERSION"
    "DEBUG"
)

# NEST-specific variables (required if NEST_ENABLED=true)
NEST_VARS=(
    "NEST_PORT"
    "NEST_PUBLIC_URL"
    "NEST_REGISTRY_URL"
    "NEST_AGENT_ID"
    "NEST_AGENT_NAME"
)

echo "========================================="
echo "Environment Validation"
echo "========================================="
echo "Checking: $ENV_FILE"
echo ""

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}✗ Environment file not found: $ENV_FILE${NC}"
    echo ""
    echo "Please create a .env file with required configuration."
    echo "You can copy .env.example as a starting point:"
    echo "  cp .env.example $ENV_FILE"
    exit 1
fi

# Load environment variables
set -a
source "$ENV_FILE"
set +a

echo "Validating required variables..."
echo ""

# Check required variables
for var in "${REQUIRED_VARS[@]}"; do
    value="${!var}"
    
    if [ -z "$value" ]; then
        echo -e "${RED}✗ $var is not set${NC}"
        VALIDATION_FAILED=1
    elif [ "$value" == "your_anthropic_api_key_here" ] || [ "$value" == "YOUR_VALUE_HERE" ]; then
        echo -e "${RED}✗ $var contains placeholder value${NC}"
        VALIDATION_FAILED=1
    else
        # Mask sensitive values
        if [[ "$var" == *"KEY"* ]] || [[ "$var" == *"SECRET"* ]]; then
            masked_value="${value:0:8}..."
            echo -e "${GREEN}✓ $var is set${NC} (${masked_value})"
        else
            echo -e "${GREEN}✓ $var is set${NC} ($value)"
        fi
    fi
done

echo ""
echo "Checking recommended variables..."
echo ""

# Check recommended variables
for var in "${RECOMMENDED_VARS[@]}"; do
    value="${!var}"
    
    if [ -z "$value" ]; then
        echo -e "${YELLOW}⚠ $var is not set (using default)${NC}"
    else
        echo -e "${GREEN}✓ $var is set${NC} ($value)"
    fi
done

# Check NEST configuration if enabled
if [ "$NEST_ENABLED" == "true" ]; then
    echo ""
    echo "NEST is enabled, checking NEST variables..."
    echo ""
    
    for var in "${NEST_VARS[@]}"; do
        value="${!var}"
        
        if [ -z "$value" ]; then
            echo -e "${RED}✗ $var is not set (required when NEST_ENABLED=true)${NC}"
            VALIDATION_FAILED=1
        elif [ "$value" == "YOUR_PUBLIC_IP" ] || [[ "$value" == *"YOUR_"* ]]; then
            echo -e "${RED}✗ $var contains placeholder value${NC}"
            VALIDATION_FAILED=1
        else
            echo -e "${GREEN}✓ $var is set${NC} ($value)"
        fi
    done
fi

# Validate specific values
echo ""
echo "Validating configuration values..."
echo ""

# Validate PORT
if [ -n "$PORT" ]; then
    if ! [[ "$PORT" =~ ^[0-9]+$ ]] || [ "$PORT" -lt 1 ] || [ "$PORT" -gt 65535 ]; then
        echo -e "${RED}✗ PORT must be a number between 1 and 65535${NC}"
        VALIDATION_FAILED=1
    else
        echo -e "${GREEN}✓ PORT is valid${NC}"
    fi
fi

# Validate NEST_PORT if NEST is enabled
if [ "$NEST_ENABLED" == "true" ] && [ -n "$NEST_PORT" ]; then
    if ! [[ "$NEST_PORT" =~ ^[0-9]+$ ]] || [ "$NEST_PORT" -lt 1 ] || [ "$NEST_PORT" -gt 65535 ]; then
        echo -e "${RED}✗ NEST_PORT must be a number between 1 and 65535${NC}"
        VALIDATION_FAILED=1
    else
        echo -e "${GREEN}✓ NEST_PORT is valid${NC}"
    fi
fi

# Validate HOST
if [ -n "$HOST" ]; then
    if [ "$HOST" != "0.0.0.0" ] && [ "$HOST" != "127.0.0.1" ] && [ "$HOST" != "localhost" ]; then
        echo -e "${YELLOW}⚠ HOST is set to $HOST (typically should be 0.0.0.0 for EC2)${NC}"
    else
        echo -e "${GREEN}✓ HOST is valid${NC}"
    fi
fi

# Validate ANTHROPIC_MODEL
if [ -n "$ANTHROPIC_MODEL" ]; then
    if [[ "$ANTHROPIC_MODEL" == claude-* ]]; then
        echo -e "${GREEN}✓ ANTHROPIC_MODEL format is valid${NC}"
    else
        echo -e "${YELLOW}⚠ ANTHROPIC_MODEL should start with 'claude-'${NC}"
    fi
fi

# Final result
echo ""
echo "========================================="
if [ $VALIDATION_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ Environment validation passed${NC}"
    echo "========================================="
    exit 0
else
    echo -e "${RED}✗ Environment validation failed${NC}"
    echo "========================================="
    echo ""
    echo "Please fix the errors above and try again."
    echo "Refer to .env.example for configuration guidance."
    exit 1
fi
