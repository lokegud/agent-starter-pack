#!/bin/bash
# Deploy Agent City Simulation locally using Docker Compose

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Agent City Simulation - Local Deployment${NC}"
echo "=========================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon not running. Please start Docker.${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} Prerequisites satisfied"
echo ""

# Check for .env.local
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}⚠️  .env.local not found${NC}"
    echo "Creating from template..."
    cp .env.template .env.local
    echo -e "${YELLOW}⚠️  Please edit .env.local with your API keys before continuing${NC}"
    echo "Press Enter to continue after editing, or Ctrl+C to exit"
    read
fi

# Parse deployment mode
MODE="${1:-minimal}"

case $MODE in
    minimal)
        echo "📦 Deploying: Foundation only"
        SERVICES="postgres redis zookeeper kafka"
        ;;
    core)
        echo "📦 Deploying: Foundation + Core modules"
        docker-compose --profile core up -d
        exit 0
        ;;
    rd)
        echo "📦 Deploying: Core + R&D department"
        docker-compose --profile core --profile rd up -d
        exit 0
        ;;
    all)
        echo "📦 Deploying: Full system (all departments)"
        docker-compose --profile all up -d
        exit 0
        ;;
    *)
        echo -e "${RED}❌ Unknown mode: $MODE${NC}"
        echo "Usage: $0 [minimal|core|rd|all]"
        exit 1
        ;;
esac

# Start foundation services
echo ""
echo "🔧 Starting foundation services..."
docker-compose up -d $SERVICES

# Wait for services to be healthy
echo ""
echo "⏳ Waiting for services to be ready..."

# Wait for PostgreSQL
echo -n "  PostgreSQL: "
until docker-compose exec -T postgres pg_isready -U agent_user &> /dev/null; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}✓${NC}"

# Wait for Redis
echo -n "  Redis: "
until docker-compose exec -T redis redis-cli ping | grep -q PONG &> /dev/null; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}✓${NC}"

# Wait for Kafka
echo -n "  Kafka: "
sleep 10  # Kafka takes longer to start
until docker-compose exec -T kafka kafka-topics --bootstrap-server localhost:9092 --list &> /dev/null; do
    echo -n "."
    sleep 2
done
echo -e " ${GREEN}✓${NC}"

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🔗 Access Points:"
echo "  PostgreSQL: localhost:5432"
echo "  Redis: localhost:6379"
echo "  Kafka: localhost:9092"

echo ""
echo "📚 Next Steps:"
echo "  - View logs: docker-compose logs -f [service-name]"
echo "  - Deploy core modules: ./scripts/deployment/deploy-local.sh core"
echo "  - Deploy with R&D: ./scripts/deployment/deploy-local.sh rd"
echo "  - Deploy full system: ./scripts/deployment/deploy-local.sh all"
echo "  - Stop services: docker-compose down"

echo ""
echo -e "${GREEN}Happy building! 🎉${NC}"
