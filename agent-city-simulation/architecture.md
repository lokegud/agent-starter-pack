# Agent City Simulation - Modular Architecture

## Design Philosophy

This system is built with **modularity** at its core:
- **Core Foundation**: Essential services that everything depends on
- **Pluggable Modules**: Components that can be added/removed independently
- **Department Plugins**: R&D, Builders, Stockbrokers as independent units
- **Cloud-Native**: Runs locally via Docker, deploys to GCP seamlessly
- **AI-Deployable**: Documented so an AI agent can understand and deploy

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    DEPARTMENTS (PLUGINS)                 │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐        │
│  │   R&D    │  │ Builders │  │ Stockbrokers   │        │
│  │ Department│  │Department│  │  Department    │        │
│  └────┬─────┘  └────┬─────┘  └────┬───────────┘        │
└───────┼─────────────┼─────────────┼────────────────────┘
        │             │             │
┌───────┼─────────────┼─────────────┼────────────────────┐
│       │       CORE MODULES        │                     │
│  ┌────▼─────┐  ┌───▼──────┐  ┌──▼─────────┐           │
│  │Identity  │  │Predictor │  │  Ranker    │           │
│  │Generator │  │          │  │            │           │
│  └──────────┘  └──────────┘  └────────────┘           │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐            │
│  │Cartogra- │  │Orchestr-  │  │  Data    │            │
│  │pher      │  │ator       │  │Integration│           │
│  └──────────┘  └───────────┘  └──────────┘            │
└───────────────────┼─────────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────────┐
│                  FOUNDATION LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Message  │  │ Database │  │   API    │             │
│  │  Queue   │  │ Services │  │ Gateway  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Cache   │  │  Logging │  │Monitoring│             │
│  │  Layer   │  │  System  │  │  System  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

## Project Structure (Modular)

```
agent-city-simulation/
├── docs/                          # All documentation
│   ├── architecture.md            # This file
│   ├── deployment/                # Deployment guides
│   │   ├── local-setup.md        # Run locally with Docker
│   │   ├── gcp-deployment.md     # Deploy to GCP
│   │   └── ai-agent-guide.md     # For AI agent auto-deployment
│   ├── modules/                   # Module documentation
│   │   ├── core-foundation.md    # Foundation services
│   │   ├── identity-generator.md # Identity system
│   │   ├── cartographer.md       # City simulation
│   │   ├── orchestrator.md       # Agent orchestration
│   │   ├── predictor.md          # Prediction system
│   │   └── ranker.md             # Ranking system
│   └── departments/               # Department documentation
│       ├── rd-department.md      # R&D agents
│       ├── builder-department.md # Builder agents
│       └── broker-department.md  # Stockbroker agents
│
├── infrastructure/                # Infrastructure as Code
│   ├── docker/                   # Docker configurations
│   │   ├── docker-compose.yml    # Local development
│   │   ├── docker-compose.prod.yml # Production-like local
│   │   └── Dockerfile.*          # Individual service Dockerfiles
│   ├── terraform/                # GCP infrastructure (Terraform)
│   │   ├── main.tf              # GCP resources
│   │   ├── gke-cluster.tf       # Kubernetes cluster
│   │   ├── databases.tf         # Cloud SQL, Memorystore
│   │   └── networking.tf        # VPC, load balancers
│   └── kubernetes/               # Kubernetes manifests
│       ├── core/                # Core services
│       ├── modules/             # Module deployments
│       └── departments/         # Department deployments
│
├── core/                         # Core foundation services
│   ├── foundation/              # Base infrastructure
│   │   ├── message_queue/       # Kafka/Pub-Sub wrapper
│   │   ├── database/            # Database connections
│   │   ├── cache/               # Redis wrapper
│   │   ├── logging/             # Structured logging
│   │   └── monitoring/          # Metrics and health
│   ├── api_gateway/             # API Gateway service
│   └── shared/                  # Shared utilities
│       ├── config/              # Configuration management
│       ├── models/              # Shared data models
│       └── utils/               # Helper functions
│
├── modules/                      # Core modules (pluggable)
│   ├── identity_generator/      # Identity generation module
│   │   ├── service/            # Main service code
│   │   ├── api/                # REST API
│   │   ├── models/             # Data models
│   │   ├── generators/         # Generation logic
│   │   └── tests/              # Unit tests
│   ├── cartographer/           # City simulation module
│   │   ├── service/
│   │   ├── api/
│   │   ├── city_engine/        # City generation
│   │   └── spatial/            # PostGIS operations
│   ├── orchestrator/           # Agent orchestration module
│   │   ├── service/
│   │   ├── agent_manager/      # Thread management
│   │   ├── scheduler/          # Task scheduling
│   │   └── coordination/       # Agent coordination
│   ├── predictor/              # Prediction module
│   │   ├── service/
│   │   ├── data_collection/    # Data gathering
│   │   ├── analysis/           # AI analysis
│   │   └── forecasting/        # Predictions
│   ├── ranker/                 # Ranking module
│   │   ├── service/
│   │   ├── scoring/            # Scoring algorithms
│   │   └── evaluation/         # Evaluation logic
│   └── data_integration/       # External data module
│       ├── service/
│       ├── connectors/         # API connectors
│       │   ├── alpaca/         # Trading API
│       │   ├── polygon/        # Market data
│       │   ├── news/           # News APIs
│       │   └── social/         # Social media
│       └── adapters/           # Data adapters
│
├── departments/                 # Department plugins
│   ├── base/                   # Base department interface
│   │   ├── department.py       # Abstract department
│   │   └── agent_base.py       # Base agent class
│   ├── rd/                     # R&D Department
│   │   ├── service/
│   │   ├── agents/            # R&D agent types
│   │   ├── research/          # Research logic
│   │   └── reports/           # Report generation
│   ├── builders/              # Builder Department
│   │   ├── service/
│   │   ├── agents/            # Builder agent types
│   │   ├── planning/          # Product planning
│   │   └── development/       # Build simulation
│   └── stockbrokers/          # Stockbroker Department
│       ├── service/
│       ├── agents/            # Broker agent types
│       ├── strategies/        # Trading strategies
│       ├── risk/              # Risk management
│       └── portfolio/         # Portfolio management
│
├── dashboard/                  # Web dashboard
│   ├── frontend/              # React/Vue frontend
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── views/
│   │   │   └── api/
│   │   └── package.json
│   └── backend/               # Dashboard API
│       └── api/
│
├── scripts/                    # Utility scripts
│   ├── setup/                 # Setup scripts
│   │   ├── local-setup.sh     # Local environment
│   │   └── gcp-setup.sh       # GCP setup
│   ├── deployment/            # Deployment scripts
│   │   ├── deploy-local.sh
│   │   └── deploy-gcp.sh
│   └── maintenance/           # Maintenance scripts
│
├── tests/                      # Integration tests
│   ├── integration/
│   ├── e2e/
│   └── load/
│
├── .env.template              # Environment template
├── .env.local                 # Local development (gitignored)
├── .env.gcp                   # GCP production (gitignored)
├── pyproject.toml             # Python dependencies
├── requirements.txt           # Python requirements
└── README.md                  # Getting started guide
```

## Modular Design Principles

### 1. Core Foundation (Always Required)
Essential services that provide base functionality:
- **Message Queue**: Inter-service communication (Cloud Pub/Sub for GCP, Kafka locally)
- **Database Services**: PostgreSQL, Redis connections
- **API Gateway**: Single entry point, routing, auth
- **Logging System**: Centralized structured logging
- **Monitoring System**: Metrics, health checks, alerting
- **Configuration Management**: Environment-based config

### 2. Core Modules (Independently Deployable)
Each module:
- Runs as its own service
- Has its own API
- Can be developed/tested independently
- Communicates via message queue
- Can scale independently

**Available Modules:**
- `identity_generator`: Generate realistic identities
- `cartographer`: City simulation and spatial tracking
- `orchestrator`: Manage agent threads and lifecycle
- `predictor`: Analysis and forecasting
- `ranker`: Evaluation and ranking
- `data_integration`: External API connections

### 3. Department Plugins (Completely Independent)
Departments are plugins that:
- Extend the base department interface
- Register with the orchestrator
- Can be enabled/disabled via config
- Operate autonomously
- Share information via message queue

**Available Departments:**
- `rd`: Research & Development
- `builders`: Product Development
- `stockbrokers`: Trading Operations

## Local vs. GCP Deployment

### Local Development (Docker Compose)
```yaml
# docker-compose.yml
services:
  # Foundation
  postgres:
    image: postgis/postgis:15
  redis:
    image: redis:7
  kafka:
    image: confluentinc/cp-kafka:7.5.0

  # Core Modules (enable as needed)
  identity-generator:
    build: ./modules/identity_generator
    depends_on: [postgres, kafka]

  cartographer:
    build: ./modules/cartographer
    depends_on: [postgres, kafka]

  # Departments (enable as needed)
  rd-department:
    build: ./departments/rd
    depends_on: [kafka]
    environment:
      - ENABLED=true  # Enable/disable easily
```

### GCP Production
```
GKE Cluster
├── Core Foundation
│   ├── Cloud Pub/Sub (managed message queue)
│   ├── Cloud SQL (PostgreSQL)
│   ├── Memorystore (Redis)
│   └── Cloud Logging (managed logging)
│
├── Core Modules (pods)
│   ├── identity-generator-deployment
│   ├── cartographer-deployment
│   └── orchestrator-deployment
│
└── Departments (pods)
    ├── rd-department-deployment
    ├── builders-department-deployment
    └── stockbrokers-department-deployment
```

## Configuration System

### Modular Configuration
```yaml
# config/core.yaml
foundation:
  message_queue:
    type: kafka  # or pubsub for GCP
    host: localhost:9092
  database:
    host: localhost
    name: agent_city

# config/modules.yaml
modules:
  identity_generator:
    enabled: true
    replicas: 2
  cartographer:
    enabled: true
    replicas: 1
  orchestrator:
    enabled: true
    replicas: 1
    max_agents: 300

# config/departments.yaml
departments:
  rd:
    enabled: true
    agent_count: 10
  builders:
    enabled: true
    agent_count: 10
  stockbrokers:
    enabled: false  # Disable until ready
    agent_count: 10
    trading_mode: paper  # or live
```

## Service Communication

### Message Queue Topics (Modular)
```
Topics organized by module/department:

Core:
- core.identity.requests
- core.identity.responses
- core.location.updates
- core.agent.lifecycle

Modules:
- predictor.forecasts
- ranker.evaluations
- cartographer.movements

Departments:
- rd.findings
- rd.requests
- builders.projects
- builders.launches
- stockbrokers.trades
- stockbrokers.analysis

Inter-Department:
- dept.rd-to-builders
- dept.rd-to-stockbrokers
```

## Deployment Modes

### Mode 1: Minimal (Development)
```bash
# Start only foundation + one module
docker-compose up postgres redis kafka identity-generator
```

### Mode 2: Core Testing
```bash
# All core modules, no departments
docker-compose up postgres redis kafka \
  identity-generator cartographer orchestrator
```

### Mode 3: Single Department
```bash
# Core + R&D department only
docker-compose --profile core --profile rd up
```

### Mode 4: Full System
```bash
# Everything
docker-compose --profile all up
```

### Mode 5: GCP Production
```bash
# Deploy to GCP via Terraform + Kubernetes
./scripts/deployment/deploy-gcp.sh --environment production
```

## Building New Modules

To add a new module:

1. **Create module directory**
   ```
   modules/new_module/
   ├── service/
   │   └── main.py
   ├── api/
   │   └── routes.py
   ├── Dockerfile
   └── module.yaml  # Module metadata
   ```

2. **Define module interface**
   ```python
   from core.shared.module import BaseModule

   class NewModule(BaseModule):
       def initialize(self):
           pass

       def health_check(self):
           pass
   ```

3. **Register with orchestrator**
   ```yaml
   # config/modules.yaml
   modules:
     new_module:
       enabled: true
   ```

4. **Add to deployment**
   ```yaml
   # docker-compose.yml
   new-module:
     build: ./modules/new_module
   ```

## AI Agent Deployment Guide

For an AI agent to deploy this system automatically, follow:
1. Read `docs/deployment/ai-agent-guide.md` (to be created)
2. Understand module dependencies from this file
3. Execute deployment scripts in order
4. Verify health checks at each stage
5. Enable modules/departments incrementally

## Next Steps

1. ✅ Architecture documented
2. ⏳ Create project structure
3. ⏳ Implement core foundation
4. ⏳ Build first module (identity_generator)
5. ⏳ Create deployment scripts
6. ⏳ Write AI agent deployment guide
