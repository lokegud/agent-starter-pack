# Agent City Simulation

A modular, cloud-native multi-agent simulation system where AI agents with realistic identities operate across autonomous departments (R&D, Builders, Stockbrokers) with real-world data integration.

## 🎯 What This Is

An autonomous agent ecosystem featuring:
- **300+ concurrent AI agents** with realistic identities
- **Three independent departments**: R&D, Builders, Stockbrokers
- **Real-world integration**: Live market data, news, trading APIs
- **City simulation**: Agents live and operate in a simulated city
- **Modular architecture**: Plug-and-play components
- **Cloud-native**: Runs locally via Docker, deploys to GCP

## 🏗️ Architecture

```
Foundation Layer → Core Modules → Departments
     ↓                 ↓              ↓
  (Always on)    (Plug & play)  (Independent)
```

See [architecture.md](./architecture.md) for detailed design.

## 📋 Prerequisites

### For Local Development
- Docker 24+ and Docker Compose
- Python 3.11+
- 16GB RAM minimum (for 300 agents)
- 50GB free disk space

### For GCP Deployment
- Google Cloud SDK (`gcloud`)
- Terraform 1.6+
- kubectl
- GCP Project with billing enabled

## 🚀 Quick Start (Local)

### 1. Clone and Setup
```bash
git clone <repository>
cd agent-city-simulation

# Copy environment template
cp .env.template .env.local

# Edit .env.local with your API keys
nano .env.local
```

### 2. Start Foundation Services
```bash
# Start core infrastructure
docker-compose up -d postgres redis kafka

# Verify services are healthy
docker-compose ps
```

### 3. Start Core Modules
```bash
# Start identity generator and cartographer
docker-compose up -d identity-generator cartographer

# Check logs
docker-compose logs -f identity-generator
```

### 4. Enable Departments (Optional)
```bash
# Start R&D department
docker-compose --profile rd up -d

# Start all departments
docker-compose --profile all up -d
```

### 5. Access Dashboard
```bash
# Start dashboard
docker-compose up -d dashboard

# Open in browser
open http://localhost:3000
```

## 🔧 Configuration

The system is configured through modular YAML files:

- `config/core.yaml` - Foundation services
- `config/modules.yaml` - Core modules (enable/disable)
- `config/departments.yaml` - Department plugins
- `.env.local` - Secrets and API keys

### Enabling/Disabling Components

Edit `config/modules.yaml`:
```yaml
modules:
  identity_generator:
    enabled: true
  cartographer:
    enabled: true
  predictor:
    enabled: false  # Disable predictor
```

Edit `config/departments.yaml`:
```yaml
departments:
  rd:
    enabled: true
    agent_count: 10
  stockbrokers:
    enabled: false  # Disable trading for now
```

## 📦 Project Structure

```
agent-city-simulation/
├── docs/              # Documentation
├── infrastructure/    # Docker, Terraform, K8s configs
├── core/              # Foundation services
├── modules/           # Core modules (pluggable)
├── departments/       # Department plugins
├── dashboard/         # Web UI
└── scripts/           # Deployment scripts
```

See [architecture.md](./architecture.md) for complete structure.

## 🌐 GCP Deployment

### 1. Setup GCP Project
```bash
# Set your GCP project
export GCP_PROJECT_ID="your-project-id"
gcloud config set project $GCP_PROJECT_ID

# Enable required APIs
./scripts/setup/gcp-setup.sh
```

### 2. Deploy Infrastructure
```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

### 3. Deploy Application
```bash
# Configure kubectl for GKE
gcloud container clusters get-credentials agent-city-cluster --region us-central1

# Deploy services
./scripts/deployment/deploy-gcp.sh --environment production
```

### 4. Verify Deployment
```bash
# Check pod status
kubectl get pods --all-namespaces

# Check services
kubectl get services

# View dashboard
kubectl port-forward svc/dashboard 3000:3000
```

## 🧪 Development

### Running Tests
```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# Load tests (300 agents)
pytest tests/load/
```

### Adding a New Module
```bash
# Create module structure
./scripts/setup/create-module.sh my_module

# Edit module code
cd modules/my_module/service

# Add to config
echo "  my_module:\n    enabled: true" >> config/modules.yaml

# Test locally
docker-compose up my-module
```

### Adding a New Department
```bash
# Create department
./scripts/setup/create-department.sh my_department

# Implement agents
cd departments/my_department/agents

# Enable in config
nano config/departments.yaml
```

## 📚 Documentation

- [Architecture Overview](./architecture.md)
- [Infrastructure Details](./infrastructure.md)
- [Project Rules](./rules.md)
- [Implementation Roadmap](./todolist.md)

### Module Documentation
- [Identity Generator](./docs/modules/identity-generator.md)
- [Cartographer](./docs/modules/cartographer.md)
- [Orchestrator](./docs/modules/orchestrator.md)
- [Predictor](./docs/modules/predictor.md)
- [Ranker](./docs/modules/ranker.md)

### Department Documentation
- [R&D Department](./docs/departments/rd-department.md)
- [Builder Department](./docs/departments/builder-department.md)
- [Stockbroker Department](./docs/departments/broker-department.md)

### Deployment Documentation
- [Local Setup Guide](./docs/deployment/local-setup.md)
- [GCP Deployment Guide](./docs/deployment/gcp-deployment.md)
- [AI Agent Deployment Guide](./docs/deployment/ai-agent-guide.md) ⭐

## 🤖 AI Agent Auto-Deployment

This system is designed to be deployable by an AI agent. See the [AI Agent Deployment Guide](./docs/deployment/ai-agent-guide.md) for:
- Step-by-step deployment instructions
- Dependency resolution
- Health check verification
- Troubleshooting procedures

## 🔐 Security

- All secrets in environment variables (never committed)
- API keys encrypted at rest
- TLS for all service communication
- Network isolation via VPC
- Trading circuit breakers and limits

See [rules.md](./rules.md) for security policies.

## 💰 Cost Estimates

### Local Development
- Free (uses local resources)

### GCP Production (Monthly)
- GKE Cluster: ~$200-400
- Cloud SQL (PostgreSQL): ~$100-200
- Memorystore (Redis): ~$50-100
- Pub/Sub: ~$50
- API Costs (Claude, Trading, News): ~$500-2000
- **Total: ~$900-2700/month**

Optimize costs:
- Use preemptible nodes
- Scale down during off-hours
- Cache aggressively
- Use free API tiers

## 📊 Monitoring

Access monitoring dashboards:
- **Local**: http://localhost:9090 (Prometheus) / http://localhost:3001 (Grafana)
- **GCP**: Cloud Console → Monitoring

Key metrics:
- Agent count and health
- Trading P&L
- API usage and costs
- System resource usage
- Error rates

## 🆘 Troubleshooting

### Services won't start
```bash
# Check Docker resources
docker system df

# Check service logs
docker-compose logs <service-name>

# Restart services
docker-compose restart
```

### Database connection issues
```bash
# Verify PostgreSQL is running
docker-compose ps postgres

# Test connection
docker-compose exec postgres psql -U agent_user -d agent_city
```

### Agent errors
```bash
# View agent logs
docker-compose logs orchestrator

# Check agent status
curl http://localhost:8000/api/agents/status
```

## 🤝 Contributing

1. Follow the modular architecture
2. Document all code (AI agent must understand)
3. Write tests for new features
4. Follow the rules in [rules.md](./rules.md)
5. No mock data in production

## 📝 License

[Your License Here]

## 🔗 Links

- [Project Vision](./prompt.md)
- [Implementation Roadmap](./todolist.md)
- [Architecture Details](./architecture.md)
- [Infrastructure Guide](./infrastructure.md)
- [Project Rules](./rules.md)

---

Built with modularity and AI-first principles. Every component is documented for both human and AI agent understanding.
