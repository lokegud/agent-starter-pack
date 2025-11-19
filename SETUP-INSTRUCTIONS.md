# Agent City - Setup Instructions

## ✅ What's Been Done

We've set up the foundation:
- ✅ Python virtual environment created (`venv/`)
- ✅ All dependencies installed (anthropic, google-cloud-aiplatform, asyncpg, redis, etc.)
- ✅ Configuration files created (`.env`, `config.yaml`)
- ✅ Docker Compose file created (`docker-compose.yml`)
- ✅ Database schema created (`agent-city-simulation/sql/mvp_schema.sql`)
- ✅ Base agent class created (`agent-city-simulation/core/agents/base_agent.py`)
- ✅ Database connection module created (`agent-city-simulation/core/database/connection.py`)
- ✅ Test scripts created

## 🚀 Next Steps (Run These On Your Local Terminal)

### **STEP 1: Configure API Keys**

Edit the `.env` file and add your actual API keys:

```bash
# Open .env file in your editor
nano .env  # or: vim .env, code .env, etc.
```

**Required changes:**
1. **ANTHROPIC_API_KEY**: Get from https://console.anthropic.com/
   - Sign up if you haven't
   - Go to "API Keys"
   - Create new key (starts with `sk-ant-`)
   - Replace `your-anthropic-key-here` with actual key

2. **GOOGLE_CLOUD_PROJECT**: Your GCP project ID
   - Find in GCP Console (top of page, project dropdown)
   - Replace `your-gcp-project-id` with actual project ID

3. **GOOGLE_APPLICATION_CREDENTIALS**: Path to service account key
   - We'll set this up in Step 3

### **STEP 2: Start Docker Services**

**Important:** You need to run these commands on your LOCAL terminal (loke@loke-asus-max), not in this environment.

```bash
# Navigate to project directory
cd ~/agent-starter-pack

# Start PostgreSQL and Redis
docker compose up -d

# Verify services are running
docker compose ps

# Should show:
# agent_city_db      postgres:15     Up      5432/tcp
# agent_city_redis   redis:7-alpine  Up      6379/tcp
```

### **STEP 3: Set Up GCP Service Account**

You need a service account to use Vertex AI (for image generation).

**On your local terminal:**

```bash
# 1. Install gcloud CLI if you haven't
# Follow: https://cloud.google.com/sdk/docs/install

# 2. Login to GCP
gcloud auth login

# 3. Set your project
gcloud config set project YOUR_PROJECT_ID

# 4. Create service account
gcloud iam service-accounts create agent-city-sa \
    --display-name="Agent City Service Account"

# 5. Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:agent-city-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# 6. Create and download key
gcloud iam service-accounts keys create ~/agent-city-key.json \
    --iam-account=agent-city-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com

# 7. Update .env file
# Set GOOGLE_APPLICATION_CREDENTIALS=/home/loke/agent-city-key.json
```

### **STEP 4: Load Database Schema**

**On your local terminal:**

```bash
cd ~/agent-starter-pack

# Load the schema into PostgreSQL
docker exec -i agent_city_db psql -U agent_user -d agent_city < agent-city-simulation/sql/mvp_schema.sql

# Verify tables were created
docker exec -it agent_city_db psql -U agent_user -d agent_city -c "\dt"

# Should show tables: scout_findings, scout_runs, ideas, products, outcomes, agent_logs, etc.
```

### **STEP 5: Test Claude API**

**On your local terminal:**

```bash
cd ~/agent-starter-pack

# Activate virtual environment
source venv/bin/activate

# Run test
python test_claude.py

# Should see:
# ✅ SUCCESS! Claude API is working!
# Claude says: Hello from Agent City! ...
```

### **STEP 6: Test Database Connection**

Create a simple test:

```bash
# Create test script
cat > test_database.py << 'EOF'
#!/usr/bin/env python3
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_db():
    conn = await asyncpg.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DB')
    )

    # Test query
    result = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")

    print("✅ Database connected!")
    print("\nTables found:")
    for row in result:
        print(f"  - {row['table_name']}")

    await conn.close()

asyncio.run(test_db())
EOF

# Run test
python test_database.py
```

## 📊 Status Check

After completing all steps, you should have:

- ✅ PostgreSQL running with Agent City schema
- ✅ Redis running
- ✅ Claude API working
- ✅ GCP credentials configured
- ✅ Virtual environment activated

## 🎯 What's Next?

Once all tests pass, we'll build the first **Scout Agent** to start finding opportunities from Reddit and ProductHunt!

---

## 🆘 Troubleshooting

### Docker won't start
```bash
# Check Docker is running
docker ps

# Restart Docker service
sudo systemctl restart docker  # Linux
# or restart Docker Desktop (Mac/Windows)
```

### API key errors
```bash
# Verify .env file
cat .env | grep ANTHROPIC

# Make sure it's loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY'))"
```

### Database connection errors
```bash
# Check PostgreSQL is running
docker compose ps

# View logs
docker compose logs postgres

# Restart if needed
docker compose restart postgres
```

### GCP/Vertex AI errors
```bash
# Verify credentials
cat $GOOGLE_APPLICATION_CREDENTIALS

# Test authentication
gcloud auth list

# Check project
gcloud config get-value project
```

---

**You're almost there! Once these steps are complete, we can start building scouts.** 🚀
