# Agent City - Quick Start Guide

## 🚀 Start Building RIGHT NOW (2 Hours)

Follow these steps to go from "nothing" to "running code" today.

---

## ✅ Pre-Flight Checklist

Before starting, make sure you have:
- [ ] Computer with internet
- [ ] Credit/debit card (for GCP verification - won't be charged)
- [ ] Email address
- [ ] 2 hours of focused time

---

## 📝 Step-by-Step Setup

### **STEP 1: Get Google Cloud Platform Account** (15 min)

1. Go to: https://console.cloud.google.com/
2. Click "Get started for free"
3. Sign in with Google account (or create one)
4. Fill out billing info (credit card for verification)
   - **Won't be charged** unless you explicitly upgrade
   - Gets you $300 free credits for 90 days
5. Accept terms and conditions
6. Wait for account activation (usually instant)

**Verify**: You should see GCP Console dashboard

---

### **STEP 2: Enable Required APIs** (5 min)

In GCP Console:

1. Go to "APIs & Services" → "Library"
2. Search and enable these APIs:
   - **Vertex AI API** (for image generation)
   - **Cloud Storage API**
   - **Compute Engine API** (if deploying to cloud)

**Verify**: Each API shows "Enabled" status

---

### **STEP 3: Get Anthropic API Key** (10 min)

1. Go to: https://console.anthropic.com/
2. Sign up for account
3. Go to "API Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)
6. Save it somewhere safe (you'll need it in Step 6)

**Cost**: Pay-as-you-go, ~$0.25-1.00 per 1000 calls for Claude 3.5 Sonnet

---

### **STEP 4: Set Up Local Development** (20 min)

**Install Required Software**:

**On Mac**:
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11+
brew install python@3.11

# Install Docker Desktop
# Download from: https://www.docker.com/products/docker-desktop/

# Install Git (if not installed)
brew install git
```

**On Ubuntu/Linux**:
```bash
# Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Git
sudo apt install git
```

**On Windows**:
```powershell
# Install Python from: https://www.python.org/downloads/
# Install Docker Desktop from: https://www.docker.com/products/docker-desktop/
# Install Git from: https://git-scm.com/download/win
```

**Verify installations**:
```bash
python3 --version  # Should show 3.11+
docker --version   # Should show Docker version
git --version      # Should show Git version
```

---

### **STEP 5: Clone Repository & Set Up Project** (10 min)

```bash
# Navigate to where you want the project
cd ~/projects  # or wherever you keep code

# Clone the repo (if not already done)
git clone https://github.com/your-username/agent-starter-pack.git
cd agent-starter-pack

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install core dependencies
pip install --upgrade pip
pip install anthropic python-dotenv pyyaml httpx
```

**Verify**: You should see `(venv)` in your terminal prompt

---

### **STEP 6: Create Configuration Files** (10 min)

**Create `.env` file** (secrets):
```bash
# In agent-starter-pack directory
cat > .env << 'EOF'
# Anthropic API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Google Cloud (get from GCP Console → IAM → Service Accounts)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json

# Database (for local Docker)
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=change_this_password
POSTGRES_DB=agent_city

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
EOF
```

**Replace these values**:
- `ANTHROPIC_API_KEY`: Your key from Step 3
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID (find in GCP Console)
- `your-key-here`: Your actual Anthropic key

**Create `config.yaml`** (settings):
```bash
cat > agent-city-simulation/config.yaml << 'EOF'
# Agent City Configuration

# Core Settings
environment: development
log_level: INFO

# Anthropic API
anthropic:
  model: claude-3-5-sonnet-20241022
  max_tokens: 4096
  temperature: 0.7

# Google Cloud / Vertex AI
vertex_ai:
  model: imagegeneration@005
  region: us-central1

# Database
database:
  host: localhost
  port: 5432
  pool_size: 10

# Redis Cache
redis:
  host: localhost
  port: 6379
  ttl: 3600

# MVP Settings
mvp:
  product_type: icon_pack
  icon_count: 50
  enabled_departments:
    - scout
    - designer
    - builder
    - tester
    - marketer
EOF
```

---

### **STEP 7: Start Infrastructure** (10 min)

**Create `docker-compose.yml`**:
```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: agent_city_db
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: agent_city_redis
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
EOF
```

**Start services**:
```bash
# Start PostgreSQL and Redis
docker-compose up -d

# Verify they're running
docker-compose ps
# Should show postgres and redis as "Up"
```

---

### **STEP 8: Test Claude API Connection** (10 min)

**Create test script**:
```bash
cat > test_claude.py << 'EOF'
#!/usr/bin/env python3
"""Test Claude API connection"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Test API call
print("Testing Claude API...")
try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Say hello and confirm you're working!"}
        ]
    )
    print("\n✅ SUCCESS! Claude says:")
    print(message.content[0].text)
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nCheck your ANTHROPIC_API_KEY in .env file")

EOF

# Make it executable
chmod +x test_claude.py

# Run test
python test_claude.py
```

**Expected output**:
```
Testing Claude API...

✅ SUCCESS! Claude says:
Hello! I'm working perfectly! ...
```

---

### **STEP 9: Create Database Schema** (10 min)

**Create schema file**:
```bash
mkdir -p agent-city-simulation/sql

cat > agent-city-simulation/sql/mvp_schema.sql << 'EOF'
-- Agent City MVP Database Schema

-- Ideas table
CREATE TABLE IF NOT EXISTS ideas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    source VARCHAR(100),
    score DECIMAL(3,2),
    status VARCHAR(20) DEFAULT 'pending',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    idea_id UUID REFERENCES ideas(id),
    product_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'designing',
    files JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Outcomes table
CREATE TABLE IF NOT EXISTS outcomes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID REFERENCES products(id),
    revenue DECIMAL(10,2) DEFAULT 0,
    sales_count INT DEFAULT 0,
    views INT DEFAULT 0,
    feedback TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Agent logs table
CREATE TABLE IF NOT EXISTS agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_type VARCHAR(50),
    task VARCHAR(255),
    status VARCHAR(20),
    input JSONB,
    output JSONB,
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_ideas_status ON ideas(status);
CREATE INDEX idx_ideas_score ON ideas(score DESC);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_idea ON products(idea_id);
CREATE INDEX idx_outcomes_product ON outcomes(product_id);
CREATE INDEX idx_agent_logs_type ON agent_logs(agent_type);
CREATE INDEX idx_agent_logs_created ON agent_logs(created_at DESC);
EOF
```

**Load schema**:
```bash
# Load into database
docker exec -i agent_city_db psql -U agent_user -d agent_city < agent-city-simulation/sql/mvp_schema.sql

# Verify tables created
docker exec -it agent_city_db psql -U agent_user -d agent_city -c "\dt"
```

**Expected output**: Should list all tables (ideas, products, outcomes, agent_logs)

---

### **STEP 10: Create Base Agent Class** (20 min)

```bash
mkdir -p agent-city-simulation/core/agents

cat > agent-city-simulation/core/agents/base_agent.py << 'EOF'
"""Base Agent class for all Agent City agents"""

import os
import logging
from typing import Dict, Any, Optional
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all agents"""

    def __init__(self, agent_type: str, personality: Optional[Dict] = None):
        self.agent_type = agent_type
        self.personality = personality or {"risk_tolerance": 0.5}
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"

    async def think(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Call Claude API to process a task
        """
        try:
            logger.info(f"[{self.agent_type}] Thinking about task...")

            messages = [{"role": "user", "content": prompt}]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.7,
                system=system_prompt or f"You are a {self.agent_type} agent.",
                messages=messages
            )

            result = response.content[0].text
            logger.info(f"[{self.agent_type}] Task completed")
            return result

        except Exception as e:
            logger.error(f"[{self.agent_type}] Error: {e}")
            raise

    def log_task(self, task: str, status: str, output: Any = None):
        """Log agent activity"""
        logger.info(f"[{self.agent_type}] Task: {task} | Status: {status}")
        if output:
            logger.debug(f"[{self.agent_type}] Output: {output}")
EOF
```

**Test the agent**:
```bash
cat > test_agent.py << 'EOF'
#!/usr/bin/env python3
"""Test base agent"""

import asyncio
from agent_city_simulation.core.agents.base_agent import BaseAgent


async def main():
    # Create agent
    agent = BaseAgent("test_agent", personality={"risk_tolerance": 0.7})

    # Test task
    prompt = "Generate 5 creative icon pack themes for productivity apps"
    result = await agent.think(prompt)

    print("\n✅ Agent Response:")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
EOF

python test_agent.py
```

---

## 🎉 You're Ready!

If all steps passed, you now have:
- ✅ GCP account with $300 credits
- ✅ Anthropic API working
- ✅ Local database (PostgreSQL + Redis)
- ✅ Base agent that can call Claude
- ✅ Development environment ready

---

## 📍 Where You Are

```
Current Status: Infrastructure ✅ Ready
Next Step: Build MVP pipeline (Week 1-4)
```

---

## 🚀 Next Steps

**Continue to**: `MVP-BUILD-PLAN.md` Week 1, Day 3-7 (Build pipeline agents)

Or run: `python scripts/start_mvp.py` (we'll build this next)

---

## ❓ Troubleshooting

**Docker won't start**:
```bash
# Check Docker is running
docker ps

# Restart Docker Desktop (Mac/Windows)
# or restart Docker service (Linux):
sudo systemctl restart docker
```

**API key errors**:
```bash
# Verify .env file exists and has your key
cat .env | grep ANTHROPIC

# Make sure .env is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

**Database connection errors**:
```bash
# Check PostgreSQL is running
docker-compose ps

# View logs
docker-compose logs postgres

# Restart if needed
docker-compose restart postgres
```

---

**You're now ready to build Agent City! Let's ship this thing.** 🚀
