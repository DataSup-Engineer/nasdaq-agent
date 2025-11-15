# NASDAQ Stock Agent - AWS EC2 Deployment Guide

This guide provides step-by-step instructions for deploying the NASDAQ Stock Agent to AWS EC2 instances.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [EC2 Instance Requirements](#ec2-instance-requirements)
3. [Security Group Configuration](#security-group-configuration)
4. [Initial Deployment](#initial-deployment)
5. [Environment Configuration](#environment-configuration)
6. [Service Management](#service-management)
7. [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)
8. [Updating the Application](#updating-the-application)
9. [Rollback Procedures](#rollback-procedures)

## Prerequisites

Before deploying, ensure you have:

- AWS account with EC2 access
- SSH key pair for EC2 access
- Anthropic API key for Claude
- Basic knowledge of Linux command line
- Git installed (for code updates)

## EC2 Instance Requirements

### Recommended Instance Types

| Environment | Instance Type | vCPU | Memory | Use Case |
|-------------|--------------|------|--------|----------|
| Development | t3.small | 2 | 2 GB | Testing and development |
| Production (Small) | t3.medium | 2 | 4 GB | Low to moderate traffic |
| Production (Medium) | t3.large | 2 | 8 GB | Moderate to high traffic |

### Storage Requirements

- **Root Volume**: 20 GB minimum (gp3 SSD recommended)
- **Type**: General Purpose SSD (gp3) for best price/performance
- **IOPS**: Default (3000 IOPS) is sufficient for most workloads

### Operating System

**Recommended:**
- Ubuntu 22.04 LTS (ami-0c7217cdde317cfec or latest)

**Alternative:**
- Amazon Linux 2023

## Security Group Configuration

### Required Inbound Rules

| Type | Protocol | Port | Source | Description |
|------|----------|------|--------|-------------|
| SSH | TCP | 22 | Your IP | SSH access (restrict to your IP) |
| Custom TCP | TCP | 8000 | 0.0.0.0/0 | REST API endpoint |
| Custom TCP | TCP | 6000 | 0.0.0.0/0 | NEST A2A endpoint (if enabled) |

### REST-Only Configuration

If you're not using NEST A2A communication, you only need:
- SSH (22) - Your IP only
- HTTP (8000) - 0.0.0.0/0

### NEST-Enabled Configuration

For full A2A capabilities, include all three ports above.

**Security Best Practices:**
- Always restrict SSH (port 22) to your IP address
- Consider using a VPN or bastion host for SSH access
- Use HTTPS with a reverse proxy (nginx) for production
- Regularly review and update security group rules

## Initial Deployment

### Step 1: Launch EC2 Instance

1. **Go to EC2 Dashboard** in AWS Console
2. **Click "Launch Instance"**
3. **Configure Instance:**
   - Name: `nasdaq-stock-agent-prod`
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (or as per requirements)
   - Key pair: Select or create new
   - Network: Default VPC
   - Security group: Create new or select existing (see configuration above)
   - Storage: 20 GB gp3
4. **Launch Instance**
5. **Note the Public IP address**

### Step 2: Connect to Instance

```bash
# Set correct permissions on your key file
chmod 400 your-key.pem

# Connect via SSH
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### Step 3: Transfer Application Files

**Option A: Using SCP (from local machine)**

```bash
# From your local machine
scp -i your-key.pem -r /path/to/nasdaq-agent ubuntu@<EC2_PUBLIC_IP>:~/
```

**Option B: Using Git (on EC2 instance)**

```bash
# On EC2 instance
cd ~
git clone https://github.com/your-repo/nasdaq-agent.git
cd nasdaq-agent
```

### Step 4: Run Deployment Script

```bash
# Navigate to application directory
cd ~/nasdaq-agent

# Make deployment script executable
chmod +x deploy.sh

# Run deployment script
sudo ./deploy.sh
```

The deployment script will:
- Install Python 3.11+ and system dependencies
- Create application directory at `/opt/nasdaq-agent`
- Create dedicated system user `nasdaq-agent`
- Set up Python virtual environment
- Install all Python dependencies
- Configure firewall (UFW)
- Set up systemd service
- Configure log rotation

**Expected Output:**
```
=========================================
NASDAQ Stock Agent Deployment Script
=========================================
[INFO] Installing system dependencies...
[INFO] Creating directory structure...
[INFO] Creating system user...
[INFO] Setting up Python virtual environment...
[INFO] Configuring firewall...
[INFO] Setting up systemd service...
[INFO] Setting up log rotation...
=========================================
Deployment script execution complete!
=========================================
```

## Environment Configuration

### Step 1: Create .env File

```bash
# Copy example configuration
sudo cp /opt/nasdaq-agent/.env.example /opt/nasdaq-agent/.env

# Edit configuration
sudo nano /opt/nasdaq-agent/.env
```

### Step 2: Configure Required Variables

**Minimum Required Configuration:**

```bash
# REQUIRED: Anthropic API Configuration
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Application Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
```

### Step 3: Configure NEST (Optional)

If you want to enable A2A communication:

```bash
# NEST Configuration
NEST_ENABLED=true
NEST_PORT=6000
NEST_PUBLIC_URL=http://<YOUR_EC2_PUBLIC_IP>:6000
NEST_REGISTRY_URL=http://registry.chat39.com:6900
NEST_AGENT_ID=nasdaq-stock-agent
NEST_AGENT_NAME=NASDAQ Stock Agent
```

**Important:** Replace `<YOUR_EC2_PUBLIC_IP>` with your actual EC2 public IP address.

### Step 4: Secure .env File

```bash
# Set restrictive permissions
sudo chmod 600 /opt/nasdaq-agent/.env

# Set correct ownership
sudo chown nasdaq-agent:nasdaq-agent /opt/nasdaq-agent/.env
```

### Step 5: Validate Configuration

```bash
# Run validation script
sudo /opt/nasdaq-agent/validate_env.sh /opt/nasdaq-agent/.env
```

**Expected Output:**
```
=========================================
Environment Validation
=========================================
Validating required variables...

✓ ANTHROPIC_API_KEY is set (sk-ant-...)
✓ ANTHROPIC_MODEL is set (claude-3-haiku-20240307)
✓ HOST is set (0.0.0.0)
✓ PORT is set (8000)

=========================================
✓ Environment validation passed
=========================================
```

## Service Management

### Start the Service

```bash
sudo systemctl start nasdaq-agent
```

### Check Service Status

```bash
sudo systemctl status nasdaq-agent
```

**Expected Output:**
```
● nasdaq-agent.service - NASDAQ Stock Agent
     Loaded: loaded (/etc/systemd/system/nasdaq-agent.service; enabled)
     Active: active (running) since ...
```

### Enable Auto-Start on Boot

```bash
sudo systemctl enable nasdaq-agent
```

### Stop the Service

```bash
sudo systemctl stop nasdaq-agent
```

### Restart the Service

```bash
sudo systemctl restart nasdaq-agent
```

### Disable Auto-Start

```bash
sudo systemctl disable nasdaq-agent
```

## Monitoring and Troubleshooting

### View Real-Time Logs

```bash
# System logs (journald)
sudo journalctl -u nasdaq-agent -f

# Application logs
sudo tail -f /var/log/nasdaq-agent/*.log
```

### View Recent Logs

```bash
# Last 50 lines
sudo journalctl -u nasdaq-agent -n 50

# Last hour
sudo journalctl -u nasdaq-agent --since "1 hour ago"

# Today's logs
sudo journalctl -u nasdaq-agent --since today
```

### Health Check

```bash
# Run health check script
/opt/nasdaq-agent/health_check.sh
```

**Expected Output:**
```
Checking NASDAQ Stock Agent health...
Endpoint: http://localhost:8000/health

✓ Service is healthy
  HTTP Status: 200
  Response: {"status":"healthy",...}
```

### Test Endpoints

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
curl http://localhost:8000/docs

# Test stock analysis (from external machine)
curl -X POST http://<EC2_PUBLIC_IP>:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "What do you think about Apple stock?"}'
```

### Common Issues and Solutions

#### Issue: Service fails to start

**Check logs:**
```bash
sudo journalctl -u nasdaq-agent -n 100
```

**Common causes:**
- Missing or invalid ANTHROPIC_API_KEY
- Port 8000 already in use
- Permission issues with /opt/nasdaq-agent

**Solutions:**
```bash
# Verify environment configuration
sudo /opt/nasdaq-agent/validate_env.sh /opt/nasdaq-agent/.env

# Check if port is in use
sudo netstat -tuln | grep 8000

# Check file permissions
ls -la /opt/nasdaq-agent/
```

#### Issue: Cannot connect from external IP

**Check security group:**
- Ensure port 8000 is open to 0.0.0.0/0
- Verify instance has public IP

**Check firewall:**
```bash
sudo ufw status
```

**Test from EC2 instance:**
```bash
curl http://localhost:8000/health
```

#### Issue: High memory usage

**Check resource usage:**
```bash
# Memory usage
free -h

# Process details
top -p $(pgrep -f "python main.py")
```

**Solution:** Upgrade to larger instance type (t3.large or t3.xlarge)

#### Issue: NEST A2A not working

**Verify NEST configuration:**
```bash
# Check NEST_PUBLIC_URL is correct
grep NEST_PUBLIC_URL /opt/nasdaq-agent/.env

# Test A2A endpoint
curl http://localhost:6000/a2a
```

**Check firewall:**
```bash
sudo ufw status | grep 6000
```

## Updating the Application

### Method 1: Using Update Mode (Recommended)

```bash
# Navigate to application directory
cd /opt/nasdaq-agent

# Pull latest changes (if using git)
sudo -u nasdaq-agent git pull

# Run deployment script in update mode
sudo /path/to/deploy.sh --update
```

The update script will:
- Pull latest code from git
- Update Python dependencies
- Restart the service
- Run health checks
- Verify deployment

### Method 2: Manual Update

```bash
# Stop the service
sudo systemctl stop nasdaq-agent

# Navigate to application directory
cd /opt/nasdaq-agent

# Pull latest code
sudo -u nasdaq-agent git pull

# Update dependencies
sudo -u nasdaq-agent /opt/nasdaq-agent/venv/bin/pip install -r requirements.txt --upgrade

# Restart the service
sudo systemctl start nasdaq-agent

# Verify service is running
sudo systemctl status nasdaq-agent

# Run health check
/opt/nasdaq-agent/health_check.sh
```

### Verify Update

```bash
# Check service status
sudo systemctl status nasdaq-agent

# View recent logs
sudo journalctl -u nasdaq-agent -n 50

# Test health endpoint
curl http://localhost:8000/health

# Check version (if available)
curl http://localhost:8000/ | jq '.version'
```

## Rollback Procedures

### Step 1: Stop the Service

```bash
sudo systemctl stop nasdaq-agent
```

### Step 2: Revert Code

```bash
# Navigate to application directory
cd /opt/nasdaq-agent

# View recent commits
sudo -u nasdaq-agent git log --oneline -n 10

# Checkout previous version
sudo -u nasdaq-agent git checkout <previous-commit-hash>
```

### Step 3: Reinstall Dependencies

```bash
# Reinstall dependencies for the reverted version
sudo -u nasdaq-agent /opt/nasdaq-agent/venv/bin/pip install -r requirements.txt
```

### Step 4: Restart Service

```bash
sudo systemctl start nasdaq-agent
```

### Step 5: Verify Rollback

```bash
# Check service status
sudo systemctl status nasdaq-agent

# Run health check
/opt/nasdaq-agent/health_check.sh

# View logs
sudo journalctl -u nasdaq-agent -n 50
```

## Performance Optimization

### Enable Multiple Workers

For production workloads, configure multiple Uvicorn workers:

```bash
# Edit systemd service file
sudo nano /etc/systemd/system/nasdaq-agent.service

# Update ExecStart line:
ExecStart=/opt/nasdaq-agent/venv/bin/uvicorn main:main --host 0.0.0.0 --port 8000 --workers 4

# Reload systemd and restart
sudo systemctl daemon-reload
sudo systemctl restart nasdaq-agent
```

### Monitor Resource Usage

```bash
# Real-time monitoring
htop

# Service-specific monitoring
systemctl status nasdaq-agent

# Memory usage
free -h

# Disk usage
df -h
```

## Backup and Recovery

### Backup Configuration

```bash
# Backup .env file
sudo cp /opt/nasdaq-agent/.env /opt/nasdaq-agent/.env.backup.$(date +%Y%m%d)

# Backup to S3 (optional)
aws s3 cp /opt/nasdaq-agent/.env s3://your-bucket/backups/nasdaq-agent-env-$(date +%Y%m%d)
```

### Backup Application

```bash
# Create tarball (excluding venv and logs)
sudo tar -czf nasdaq-agent-backup-$(date +%Y%m%d).tar.gz \
  --exclude='/opt/nasdaq-agent/venv' \
  --exclude='/opt/nasdaq-agent/logs' \
  /opt/nasdaq-agent
```

## Security Best Practices

1. **Restrict SSH Access**: Only allow SSH from your IP
2. **Use HTTPS**: Set up nginx reverse proxy with SSL certificates
3. **Rotate API Keys**: Regularly rotate Anthropic API keys
4. **Keep System Updated**: Run `sudo apt update && sudo apt upgrade` regularly
5. **Monitor Logs**: Regularly review logs for suspicious activity
6. **Use IAM Roles**: For AWS resource access, use IAM roles instead of access keys
7. **Enable CloudWatch**: Send logs to CloudWatch for centralized monitoring

## Support and Additional Resources

- **Application Logs**: `/var/log/nasdaq-agent/`
- **System Logs**: `sudo journalctl -u nasdaq-agent`
- **Health Check**: `/opt/nasdaq-agent/health_check.sh`
- **Environment Validation**: `/opt/nasdaq-agent/validate_env.sh`

For issues or questions, check the logs first and refer to the troubleshooting section above.
