# AI Agent Deployment Guide

**Purpose**: This guide enables an AI agent to understand, deploy, and manage the Agent City Simulation system automatically.

## For AI Agents Reading This

You are an AI agent tasked with deploying a complex multi-agent system. This guide provides:
1. **Complete understanding** of system architecture
2. **Step-by-step deployment** instructions
3. **Dependency resolution** logic
4. **Health verification** procedures
5. **Troubleshooting** decision trees

## System Overview for AI Understanding

### What You're Deploying

A **modular multi-agent simulation** with three layers:

1. **Foundation Layer** (must deploy first)
   - PostgreSQL database
   - Redis cache
   - Message queue (Kafka locally, Pub/Sub on GCP)
   - Logging and monitoring

2. **Core Modules** (can deploy in parallel after foundation)
   - `identity_generator`: Creates agent identities
   - `cartographer`: Manages city simulation
   - `orchestrator`: Coordinates 300+ agents
   - `predictor`: Market and trend analysis
   - `ranker`: Evaluation system
   - `data_integration`: External API connections

3. **Department Plugins** (deploy after orchestrator)
   - `rd`: Research & Development agents
   - `builders`: Product development agents
   - `stockbrokers`: Trading agents (requires special care)

### Key Principle: Modularity

Each component can be enabled/disabled independently through configuration files. Not all components are required for a minimal deployment.

## Deployment Decision Tree

```
START
  ↓
Are you deploying locally or to GCP?
  ├─→ LOCAL → Use Docker Compose path
  └─→ GCP → Use Terraform + Kubernetes path
  ↓
What is the deployment goal?
  ├─→ DEVELOPMENT → Minimal setup (foundation + 1-2 modules)
  ├─→ TESTING → Core modules only (no departments)
  ├─→ STAGING → Full system with paper trading
  └─→ PRODUCTION → Full system with live trading
  ↓
Execute deployment plan
  ↓
Verify health checks
  ↓
COMPLETE or TROUBLESHOOT
```

## Prerequisites Verification

Before deploying, verify these requirements:

### For Local Deployment
```bash
# Check Docker
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not installed"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "ERROR: Docker Compose not installed"
    exit 1
fi

# Check Docker is running
if ! docker info &> /dev/null; then
    echo "ERROR: Docker daemon not running"
    exit 1
fi

# Check available resources
MEMORY=$(docker info --format '{{.MemTotal}}')
if [ $MEMORY -lt 17179869184 ]; then  # 16GB
    echo "WARNING: Less than 16GB RAM available"
fi
```

### For GCP Deployment
```bash
# Check gcloud
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI not installed"
    exit 1
fi

# Check authentication
if ! gcloud auth list --filter=status:ACTIVE &> /dev/null; then
    echo "ERROR: Not authenticated with GCP"
    echo "Run: gcloud auth login"
    exit 1
fi

# Check project is set
PROJECT=$(gcloud config get-value project)
if [ -z "$PROJECT" ]; then
    echo "ERROR: GCP project not set"
    echo "Run: gcloud config set project PROJECT_ID"
    exit 1
fi

# Check Terraform
if ! command -v terraform &> /dev/null; then
    echo "ERROR: Terraform not installed"
    exit 1
fi

# Check kubectl
if ! command -v kubectl &> /dev/null; then
    echo "ERROR: kubectl not installed"
    exit 1
fi
```

## Dependency Graph

Understanding deployment order is critical. Here's the dependency graph:

```
Foundation Services (parallel)
├── postgres (no dependencies)
├── redis (no dependencies)
└── kafka/pubsub (no dependencies)
      ↓
Core Modules (some parallel)
├── identity_generator (depends: postgres, kafka)
├── cartographer (depends: postgres with PostGIS, kafka)
├── data_integration (depends: kafka, redis)
│     ↓
├── predictor (depends: kafka, data_integration)
└── ranker (depends: kafka)
      ↓
orchestrator (depends: kafka, all above modules)
      ↓
Departments (parallel)
├── rd (depends: orchestrator, predictor)
├── builders (depends: orchestrator, rd)
└── stockbrokers (depends: orchestrator, predictor, data_integration)
```

## Local Deployment (Docker Compose)

### Phase 1: Foundation Services

```bash
#!/bin/bash
# deploy-foundation.sh

set -e  # Exit on error

echo "🚀 Deploying Foundation Services..."

# Navigate to project root
cd /path/to/agent-city-simulation

# Verify .env.local exists
if [ ! -f .env.local ]; then
    echo "ERROR: .env.local not found"
    echo "Copy from template: cp .env.template .env.local"
    exit 1
fi

# Start foundation services
echo "Starting PostgreSQL..."
docker-compose up -d postgres

echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec -T postgres pg_isready -U agent_user; do
    sleep 2
done
echo "✓ PostgreSQL is ready"

# Initialize PostGIS extension
echo "Enabling PostGIS extension..."
docker-compose exec -T postgres psql -U agent_user -d agent_city -c "CREATE EXTENSION IF NOT EXISTS postgis;"
echo "✓ PostGIS enabled"

echo "Starting Redis..."
docker-compose up -d redis

echo "Waiting for Redis to be ready..."
until docker-compose exec -T redis redis-cli ping | grep -q PONG; do
    sleep 2
done
echo "✓ Redis is ready"

echo "Starting Kafka..."
docker-compose up -d zookeeper kafka

echo "Waiting for Kafka to be ready..."
sleep 10  # Kafka takes longer to start
until docker-compose exec -T kafka kafka-topics --bootstrap-server localhost:9092 --list &> /dev/null; do
    sleep 2
done
echo "✓ Kafka is ready"

# Create required Kafka topics
echo "Creating Kafka topics..."
TOPICS=(
    "core.identity.requests"
    "core.identity.responses"
    "core.location.updates"
    "core.agent.lifecycle"
    "predictor.forecasts"
    "ranker.evaluations"
    "dept.rd-findings"
    "dept.stockbrokers-trades"
)

for topic in "${TOPICS[@]}"; do
    docker-compose exec -T kafka kafka-topics --create \
        --bootstrap-server localhost:9092 \
        --topic "$topic" \
        --partitions 3 \
        --replication-factor 1 \
        --if-not-exists
done
echo "✓ Kafka topics created"

echo "✅ Foundation services deployed successfully"
```

### Phase 2: Core Modules

```bash
#!/bin/bash
# deploy-core-modules.sh

set -e

echo "🚀 Deploying Core Modules..."

# Read module configuration
ENABLED_MODULES=$(python3 -c "
import yaml
with open('config/modules.yaml') as f:
    config = yaml.safe_load(f)
for name, settings in config['modules'].items():
    if settings.get('enabled', False):
        print(name)
")

echo "Enabled modules: $ENABLED_MODULES"

# Deploy modules based on dependency order
deploy_module() {
    local module=$1
    echo "Deploying $module..."

    # Build image
    docker-compose build $module

    # Start service
    docker-compose up -d $module

    # Wait for health check
    local max_attempts=30
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -f http://localhost:${module_port}/health &> /dev/null; then
            echo "✓ $module is healthy"
            return 0
        fi
        sleep 2
        ((attempt++))
    done

    echo "ERROR: $module failed health check"
    docker-compose logs $module
    return 1
}

# Deploy in dependency order
for module in identity_generator cartographer data_integration predictor ranker orchestrator; do
    if echo "$ENABLED_MODULES" | grep -q "$module"; then
        deploy_module "$module"
    else
        echo "⊘ Skipping disabled module: $module"
    fi
done

echo "✅ Core modules deployed successfully"
```

### Phase 3: Departments

```bash
#!/bin/bash
# deploy-departments.sh

set -e

echo "🚀 Deploying Departments..."

# Check if orchestrator is healthy
if ! curl -f http://localhost:8000/health &> /dev/null; then
    echo "ERROR: Orchestrator must be running before deploying departments"
    exit 1
fi

# Read department configuration
ENABLED_DEPTS=$(python3 -c "
import yaml
with open('config/departments.yaml') as f:
    config = yaml.safe_load(f)
for name, settings in config['departments'].items():
    if settings.get('enabled', False):
        print(name)
")

echo "Enabled departments: $ENABLED_DEPTS"

# Deploy each department
for dept in $ENABLED_DEPTS; do
    echo "Deploying $dept department..."

    # Special handling for stockbrokers
    if [ "$dept" = "stockbrokers" ]; then
        # Verify trading mode
        TRADING_MODE=$(python3 -c "
import yaml
with open('config/departments.yaml') as f:
    config = yaml.safe_load(f)
print(config['departments']['stockbrokers'].get('trading_mode', 'paper'))
")

        if [ "$TRADING_MODE" = "live" ]; then
            echo "⚠️  WARNING: Live trading mode enabled"
            echo "⚠️  Real money will be used"
            read -p "Continue? (yes/no): " confirm
            if [ "$confirm" != "yes" ]; then
                echo "Skipping stockbrokers department"
                continue
            fi
        fi
    fi

    docker-compose up -d $dept-department
    echo "✓ $dept department started"
done

echo "✅ Departments deployed successfully"
```

### Complete Local Deployment Script

```bash
#!/bin/bash
# deploy-local.sh - Complete local deployment

set -e

echo "🚀 Starting Agent City Simulation Deployment (Local)"
echo "=================================================="

# Run deployment phases
./scripts/deployment/deploy-foundation.sh
echo ""

./scripts/deployment/deploy-core-modules.sh
echo ""

./scripts/deployment/deploy-departments.sh
echo ""

# Deploy dashboard
echo "🚀 Deploying Dashboard..."
docker-compose up -d dashboard
echo "✓ Dashboard started at http://localhost:3000"

# Summary
echo ""
echo "✅ Deployment Complete!"
echo "======================"
echo ""
echo "Services running:"
docker-compose ps

echo ""
echo "Access points:"
echo "  - Dashboard: http://localhost:3000"
echo "  - API Gateway: http://localhost:8000"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3001"

echo ""
echo "To view logs:"
echo "  docker-compose logs -f [service-name]"

echo ""
echo "To stop all services:"
echo "  docker-compose down"
```

## GCP Deployment (Terraform + Kubernetes)

### Phase 1: Infrastructure Provisioning

```bash
#!/bin/bash
# deploy-gcp-infrastructure.sh

set -e

echo "🚀 Provisioning GCP Infrastructure..."

cd infrastructure/terraform

# Initialize Terraform
echo "Initializing Terraform..."
terraform init

# Validate configuration
echo "Validating Terraform configuration..."
terraform validate

# Plan deployment
echo "Planning infrastructure deployment..."
terraform plan -out=tfplan

# Review plan
echo ""
echo "Review the plan above. This will create:"
echo "  - GKE cluster"
echo "  - Cloud SQL (PostgreSQL)"
echo "  - Memorystore (Redis)"
echo "  - Pub/Sub topics"
echo "  - VPC and networking"
echo "  - IAM roles and service accounts"
echo ""

read -p "Continue with deployment? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Deployment cancelled"
    exit 0
fi

# Apply infrastructure
echo "Applying infrastructure..."
terraform apply tfplan

# Get outputs
echo "Getting infrastructure outputs..."
GKE_CLUSTER=$(terraform output -raw gke_cluster_name)
GKE_REGION=$(terraform output -raw gke_region)
SQL_INSTANCE=$(terraform output -raw sql_instance_connection)

# Configure kubectl
echo "Configuring kubectl..."
gcloud container clusters get-credentials $GKE_CLUSTER --region $GKE_REGION

echo "✅ Infrastructure provisioned successfully"
```

### Phase 2: Deploy to Kubernetes

```bash
#!/bin/bash
# deploy-gcp-application.sh

set -e

echo "🚀 Deploying Application to GKE..."

cd infrastructure/kubernetes

# Create namespace
echo "Creating namespace..."
kubectl create namespace agent-city --dry-run=client -o yaml | kubectl apply -f -

# Deploy secrets
echo "Deploying secrets..."
# Read from .env.gcp and create Kubernetes secrets
kubectl create secret generic api-keys \
    --from-env-file=../../.env.gcp \
    --namespace=agent-city \
    --dry-run=client -o yaml | kubectl apply -f -

# Deploy core services
echo "Deploying core services..."
kubectl apply -f core/ --namespace=agent-city

# Wait for core services
echo "Waiting for core services to be ready..."
kubectl wait --for=condition=available --timeout=300s \
    deployment/identity-generator \
    deployment/cartographer \
    --namespace=agent-city

# Deploy modules
echo "Deploying modules..."
for module in modules/*.yaml; do
    # Check if module is enabled in config
    module_name=$(basename $module .yaml)
    if grep -q "enabled: true" ../../config/modules.yaml; then
        echo "Deploying $module_name..."
        kubectl apply -f $module --namespace=agent-city
    fi
done

# Deploy orchestrator
echo "Deploying orchestrator..."
kubectl apply -f modules/orchestrator.yaml --namespace=agent-city

kubectl wait --for=condition=available --timeout=300s \
    deployment/orchestrator \
    --namespace=agent-city

# Deploy departments
echo "Deploying departments..."
for dept in departments/*.yaml; do
    dept_name=$(basename $dept .yaml)
    if grep -q "enabled: true" ../../config/departments.yaml; then
        echo "Deploying $dept_name..."
        kubectl apply -f $dept --namespace=agent-city
    fi
done

# Deploy ingress
echo "Deploying ingress..."
kubectl apply -f ingress.yaml --namespace=agent-city

# Get external IP
echo "Waiting for external IP..."
EXTERNAL_IP=""
while [ -z $EXTERNAL_IP ]; do
    EXTERNAL_IP=$(kubectl get svc dashboard-lb \
        --namespace=agent-city \
        --template="{{range .status.loadBalancer.ingress}}{{.ip}}{{end}}")
    [ -z "$EXTERNAL_IP" ] && sleep 10
done

echo "✅ Application deployed successfully"
echo ""
echo "Dashboard URL: http://$EXTERNAL_IP"
```

## Health Check Procedures

AI agents should verify health at each stage:

### Foundation Health Checks

```python
import psycopg2
import redis
from kafka import KafkaProducer

def check_postgres_health():
    """Verify PostgreSQL is accessible"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="agent_city",
            user="agent_user",
            password="agent_pass"
        )
        conn.close()
        return True, "PostgreSQL healthy"
    except Exception as e:
        return False, f"PostgreSQL error: {str(e)}"

def check_redis_health():
    """Verify Redis is accessible"""
    try:
        r = redis.Redis(host='localhost', port=6379)
        r.ping()
        return True, "Redis healthy"
    except Exception as e:
        return False, f"Redis error: {str(e)}"

def check_kafka_health():
    """Verify Kafka is accessible"""
    try:
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.close()
        return True, "Kafka healthy"
    except Exception as e:
        return False, f"Kafka error: {str(e)}"

def verify_foundation_health():
    """Run all foundation health checks"""
    checks = [
        ("PostgreSQL", check_postgres_health),
        ("Redis", check_redis_health),
        ("Kafka", check_kafka_health)
    ]

    all_healthy = True
    for name, check in checks:
        healthy, message = check()
        print(f"{name}: {message}")
        if not healthy:
            all_healthy = False

    return all_healthy
```

### Module Health Checks

```python
import requests
import time

def check_module_health(module_name, port, max_retries=30):
    """
    Check if a module is healthy

    Args:
        module_name: Name of the module
        port: HTTP port for health endpoint
        max_retries: Maximum number of retry attempts

    Returns:
        tuple: (is_healthy, message)
    """
    url = f"http://localhost:{port}/health"

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    return True, f"{module_name} is healthy"
                else:
                    return False, f"{module_name} unhealthy: {data.get('message')}"
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                return False, f"{module_name} not responding after {max_retries} attempts"

    return False, f"{module_name} health check failed"

# Module ports (example)
MODULE_PORTS = {
    'identity_generator': 8001,
    'cartographer': 8002,
    'orchestrator': 8003,
    'predictor': 8004,
    'ranker': 8005,
    'data_integration': 8006
}

def verify_all_modules_healthy():
    """Check health of all enabled modules"""
    all_healthy = True

    for module, port in MODULE_PORTS.items():
        healthy, message = check_module_health(module, port)
        print(message)
        if not healthy:
            all_healthy = False

    return all_healthy
```

## Troubleshooting Decision Tree for AI Agents

When deployment fails, follow this decision tree:

```
FAILURE DETECTED
  ↓
Which phase failed?
  ├─→ FOUNDATION
  │     ↓
  │   Which service?
  │   ├─→ PostgreSQL
  │   │     - Check disk space
  │   │     - Check port 5432 availability
  │   │     - Review logs: docker-compose logs postgres
  │   ├─→ Redis
  │   │     - Check port 6379 availability
  │   │     - Check memory limits
  │   │     - Review logs: docker-compose logs redis
  │   └─→ Kafka
  │         - Check ports 9092, 2181 availability
  │         - Increase memory if needed
  │         - Review logs: docker-compose logs kafka
  │
  ├─→ MODULE
  │     ↓
  │   Check module logs: docker-compose logs [module-name]
  │     ↓
  │   Common issues:
  │   ├─→ Database connection failed
  │   │     - Verify foundation services healthy
  │   │     - Check database credentials in .env.local
  │   ├─→ Kafka connection failed
  │   │     - Verify Kafka is running
  │   │     - Check Kafka topics exist
  │   ├─→ Module crashes on startup
  │   │     - Check dependencies installed
  │   │     - Verify configuration files
  │   │     - Check for missing API keys
  │   └─→ Health check fails
  │         - Check module logs for errors
  │         - Verify all dependencies met
  │
  └─→ DEPARTMENT
        ↓
      Check department logs: docker-compose logs [dept]-department
        ↓
      Common issues:
      ├─→ Orchestrator not available
      │     - Verify orchestrator is running and healthy
      ├─→ API keys missing (stockbrokers)
      │     - Check .env.local has trading API keys
      ├─→ Insufficient resources
      │     - Check Docker resource limits
      │     - Reduce agent_count in config
      └─→ Department won't start
            - Check dependencies in logs
            - Verify all required modules running
```

## Rollback Procedures

If deployment fails, AI agents should roll back:

### Local Rollback
```bash
# Stop all services
docker-compose down

# Remove volumes (if corrupted)
docker-compose down -v

# Restart from known good state
git checkout [last-working-commit]
./scripts/deployment/deploy-local.sh
```

### GCP Rollback
```bash
# Rollback Kubernetes deployments
kubectl rollout undo deployment/[deployment-name] --namespace=agent-city

# Or rollback all
kubectl rollout undo deployment --all --namespace=agent-city

# If infrastructure needs rollback
cd infrastructure/terraform
terraform destroy  # WARNING: Destructive
```

## Monitoring Deployment Success

AI agents should monitor these metrics post-deployment:

```python
def verify_deployment_success():
    """Comprehensive deployment verification"""

    checks = {
        'foundation_healthy': verify_foundation_health(),
        'modules_healthy': verify_all_modules_healthy(),
        'agents_running': check_agent_count() > 0,
        'no_errors': check_error_rate() < 0.01,  # Less than 1% errors
        'api_responding': check_api_gateway(),
        'dashboard_accessible': check_dashboard_access()
    }

    success = all(checks.values())

    print("\nDeployment Verification:")
    print("=" * 50)
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check}")

    return success

def check_agent_count():
    """Get number of running agents"""
    try:
        response = requests.get('http://localhost:8000/api/agents/count')
        return response.json()['count']
    except:
        return 0

def check_error_rate():
    """Check error rate from logs"""
    # Implementation depends on logging system
    pass

def check_api_gateway():
    """Verify API gateway is responding"""
    try:
        response = requests.get('http://localhost:8000/health')
        return response.status_code == 200
    except:
        return False

def check_dashboard_access():
    """Verify dashboard is accessible"""
    try:
        response = requests.get('http://localhost:3000')
        return response.status_code == 200
    except:
        return False
```

## Configuration for Different Deployment Modes

AI agents can use these configurations:

### Minimal (Development)
```yaml
# config/modules.yaml
modules:
  identity_generator:
    enabled: true
    replicas: 1
  cartographer:
    enabled: true
    replicas: 1
  orchestrator:
    enabled: true
    max_agents: 10  # Reduced for dev

# config/departments.yaml
departments:
  rd:
    enabled: false
  builders:
    enabled: false
  stockbrokers:
    enabled: false
```

### Testing
```yaml
# config/modules.yaml
modules:
  identity_generator:
    enabled: true
  cartographer:
    enabled: true
  orchestrator:
    enabled: true
    max_agents: 50
  predictor:
    enabled: true
  ranker:
    enabled: true

# config/departments.yaml
departments:
  rd:
    enabled: true
    agent_count: 5
  builders:
    enabled: true
    agent_count: 5
  stockbrokers:
    enabled: false  # No trading in test
```

### Production
```yaml
# config/modules.yaml
modules:
  identity_generator:
    enabled: true
    replicas: 2
  cartographer:
    enabled: true
    replicas: 2
  orchestrator:
    enabled: true
    max_agents: 300
    replicas: 3
  predictor:
    enabled: true
    replicas: 2
  ranker:
    enabled: true
  data_integration:
    enabled: true
    replicas: 2

# config/departments.yaml
departments:
  rd:
    enabled: true
    agent_count: 100
  builders:
    enabled: true
    agent_count: 100
  stockbrokers:
    enabled: true
    agent_count: 100
    trading_mode: live  # CAREFUL!
    max_capital_per_agent: 500  # USD
```

## Summary for AI Agents

When deploying this system:

1. **Verify prerequisites** before starting
2. **Follow dependency order** strictly (foundation → modules → departments)
3. **Check health** after each phase
4. **Use configuration files** to enable/disable components
5. **Special care** for stockbrokers (real money!)
6. **Monitor continuously** post-deployment
7. **Rollback** if any phase fails
8. **Document** any issues encountered

The system is designed to be resilient and modular. If something fails, isolate the issue, fix it, and redeploy just that component.

---

**Note**: This guide is living documentation. As the system evolves, this guide should be updated to reflect new components, dependencies, and procedures.
