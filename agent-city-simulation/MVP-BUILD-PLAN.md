# Agent City MVP - Let's Build This Thing

## 🎯 Mission: Prove the Concept in 4 Weeks

**Goal**: Launch ONE real product autonomously and make $1 in revenue.

If we can do that, we can do it 100 times. Let's prove the pipeline works before we build the empire.

---

## 🔥 MVP Scope (Ruthlessly Minimal)

### **What We're Building**

**ONE product through the FULL pipeline**:
```
Scout finds opportunity → Evaluate it → Design it → Build it → Test it → Launch it
  ↓
Real product on real marketplace → Real money
```

**Product Type**: **Icon Pack** (simplest, proven market)
- 50 icons in one style
- SVG + PNG formats
- Launch on Gumroad ($47 price point)
- Goal: Get 1 sale (prove it works)

### **What We're NOT Building (Yet)**

❌ 300 concurrent agents (just 1-2 per stage)
❌ Full web dashboard (just logs and CLI)
❌ Meta-Orchestrator (manual optimization for now)
❌ Stockbrokers Department (no money yet)
❌ Multiple products at once (one product, prove it works)
❌ Complex personality system (simplified: low/medium/high risk tolerance)
❌ Fancy UI (we're not the users, output is the product)

---

## 🏗️ MVP Architecture (4 Weeks)

### **Week 1: Foundation** (Days 1-7)
**Goal**: Get basic infrastructure running

**Day 1-2: Setup**
```yaml
infrastructure:
  - "GCP account + free credits"
  - "Docker Compose locally"
  - "PostgreSQL (1 database, simplified schema)"
  - "Redis (basic caching)"
  - "Python project structure"

deliverable: "Can store data, run code locally"
test: "Write a record to DB, read it back"
```

**Day 3-5: Core Agent Framework**
```yaml
build:
  - "Base Agent class (with Claude API integration)"
  - "Simple state machine (pending → in_progress → completed)"
  - "Logging (just print statements + file for now)"
  - "Configuration (YAML files)"

deliverable: "Can create an agent, give it a task, get a result"
test: "Agent calls Claude API, returns response, logs it"
```

**Day 6-7: Database Schema (Minimal)**
```sql
-- Just the essentials
CREATE TABLE ideas (
    id UUID PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    source VARCHAR(100),
    score DECIMAL(3,2),
    status VARCHAR(20),
    created_at TIMESTAMP
);

CREATE TABLE products (
    id UUID PRIMARY KEY,
    idea_id UUID REFERENCES ideas(id),
    product_type VARCHAR(50),
    status VARCHAR(20),
    files JSONB,
    created_at TIMESTAMP
);

CREATE TABLE outcomes (
    id UUID PRIMARY KEY,
    product_id UUID REFERENCES products(id),
    revenue DECIMAL(10,2),
    sales_count INT,
    created_at TIMESTAMP
);
```

**Week 1 Deliverable**: ✅ Can run agents locally, store results in DB

---

### **Week 2: Pipeline (Simplified)** (Days 8-14)
**Goal**: Get one idea through to a designed product

**Simplified Departments** (1-2 agents each):

**Day 8-9: Scout Agent** (Idea Factory - Manual Seed)
```yaml
approach: "Skip auto-scouting for MVP"
manual_seed:
  - "YOU provide 3 trending icon topics from ProductHunt/Twitter"
  - "Agent researches each topic (Google search, analyze competition)"
  - "Agent scores each idea (simple 0-1 score)"
  - "Picks highest scoring"

deliverable: "One vetted icon pack idea in database"
example: "Productivity app icons (minimalist, pastel colors)"
```

**Day 10-11: Designer Agent**
```yaml
task:
  - "Takes idea: 'Productivity app icons'"
  - "Uses Claude to generate: icon list (50 specific icons)"
  - "Defines style guide (colors, line width, corner radius)"
  - "Outputs: design_spec.json"

deliverable: "Design specification ready for generation"
example_output:
  icons: ["calendar", "checklist", "timer", "notification", ...]
  style:
    colors: ["#A8DADC", "#F1FAEE", "#E63946"]
    style: "minimalist line art"
    size: "512x512px"
```

**Day 12-14: Builder Agent** (The Critical Part)
```yaml
task:
  - "Reads design_spec.json"
  - "For each icon: Generate using Vertex AI Imagen"
  - "Saves PNG files"
  - "Converts to SVG (using potrace or vectorization)"
  - "Packages: ZIP file with all icons"

deliverable: "50 icons generated, packaged, ready to sell"
tools:
  - "Vertex AI Imagen API (free with GCP credits)"
  - "Python PIL/Pillow (image processing)"
  - "cairosvg or potrace (PNG → SVG)"
```

**Week 2 Deliverable**: ✅ One icon pack designed and generated

---

### **Week 3: Quality & Launch** (Days 15-21)
**Goal**: Test, package, and launch on Gumroad

**Day 15-16: Tester Agent**
```yaml
task:
  - "Visual consistency check (all icons same style?)"
  - "File format validation (PNG/SVG valid?)"
  - "Naming convention (consistent?)"
  - "Size validation (all 512x512?)"
  - "Generate quality report"

deliverable: "PASS/FAIL + list of issues"
if_fail: "Send back to Builder with specific fixes"
```

**Day 17-18: Marketing Agent** (Simplified Salesman)
```yaml
task:
  - "Generate product description (Claude writes copy)"
  - "Create preview images (grid of 12 icons)"
  - "Write SEO keywords"
  - "Draft social media post"

deliverable: "Marketing package ready for Gumroad"
```

**Day 19-20: Launch**
```yaml
task:
  - "Create Gumroad product (manual for MVP, automate later)"
  - "Upload icon pack ZIP"
  - "Add description, preview images"
  - "Set price: $47"
  - "Publish"

deliverable: "Live product on Gumroad"
url: "gumroad.com/l/your-icon-pack"
```

**Day 21: Marketing Push**
```yaml
channels:
  - "Post on Twitter (your personal account)"
  - "Post on Reddit (r/SideProject, r/UI_Design)"
  - "Submit to ProductHunt (optional)"
  - "Share in relevant Discord/Slack communities"

goal: "Get EYES on the product"
success: "Get 1 sale (even if it's from your friend!)"
```

**Week 3 Deliverable**: ✅ Product launched, first sale attempt

---

### **Week 4: Learning & Iteration** (Days 22-28)
**Goal**: Learn from outcomes, improve pipeline

**Day 22-24: Outcome Tracking**
```yaml
monitor:
  - "Gumroad sales (check daily)"
  - "Gumroad analytics (views, clicks)"
  - "Social media engagement"

record:
  - "Revenue: $X"
  - "Sales: Y"
  - "Feedback: Z comments"

deliverable: "Outcome data in database"
```

**Day 25-27: Retrospective**
```yaml
questions:
  - "Did it work? (Did we get a sale?)"
  - "If yes: What worked? Double down."
  - "If no: Why not? What to fix?"

improvements:
  quality: "Were icons good enough?"
  marketing: "Did anyone see it?"
  pricing: "Was $47 right?"
  positioning: "Right target audience?"

deliverable: "Lessons learned document"
```

**Day 28: Plan Next Product**
```yaml
if_success:
  - "Launch product #2 (same pipeline, faster)"
  - "Different icon theme or template product"
  - "Improve pipeline based on learnings"

if_failure:
  - "Diagnose: Was it quality? Marketing? Product choice?"
  - "Fix critical issues"
  - "Try again with improvements"

deliverable: "Go/no-go decision + next steps"
```

**Week 4 Deliverable**: ✅ Lessons learned, decision on scaling

---

## 💻 Tech Stack (MVP)

### **Infrastructure** (Run Locally First)
```yaml
local_dev:
  database: "PostgreSQL via Docker"
  cache: "Redis via Docker"
  code: "Python 3.11+"
  api: "Claude API (Anthropic)"
  image_gen: "Vertex AI Imagen (GCP)"

cost: "$0 (using free credits)"
```

### **Cloud Deployment** (Week 2-3, if needed)
```yaml
gcp_services:
  compute: "Cloud Run (2M requests free/month)"
  database: "Cloud SQL (but start with Docker locally)"
  storage: "Cloud Storage (5GB free)"

deploy_only_if: "Local works and you want to run 24/7"
```

### **Python Stack**
```yaml
core:
  - "anthropic: Claude API"
  - "google-cloud-aiplatform: Vertex AI"
  - "asyncpg: PostgreSQL async"
  - "redis-py: Redis"
  - "pydantic: Config management"

image_processing:
  - "pillow: Image manipulation"
  - "cairosvg: SVG conversion"

utilities:
  - "httpx: HTTP requests"
  - "pyyaml: Config files"
  - "python-dotenv: Environment variables"
```

---

## 📊 Success Metrics (MVP)

### **Week 1**: ✅ Infrastructure running
- Can run agents locally
- Can store data in PostgreSQL
- Can call Claude API

### **Week 2**: ✅ Pipeline working
- Idea → Design → Build works
- 50 icons generated
- Files packaged

### **Week 3**: ✅ Product launched
- Live on Gumroad
- Marketing posted
- First views recorded

### **Week 4**: ✅ Revenue OR clear learnings
- **Best case**: $1+ revenue (prove concept works!)
- **Good case**: 0 sales but 100+ views (product OK, need better marketing)
- **Learning case**: 0 sales, <10 views (improve product or marketing)
- **Worst case**: Pipeline broken (but we learn what to fix)

---

## 💰 Cost Estimate (4 Weeks)

```yaml
mandatory:
  anthropic_api: "$20-50" # Claude API calls
  vertex_ai: "$0" # Free with GCP credits
  gcp_compute: "$0" # Free tier
  gumroad: "$0" # Free (pay 10% on sales)
  domain: "$0" # Use Gumroad subdomain for MVP

total_mandatory: "$20-50"

optional:
  domain_name: "$12" # If you want yourname.com
  cloud_deploy: "$0" # Still free tier

total_with_optional: "$32-62"
```

**You can test the entire concept for $20-50.**

---

## 🎯 Key Decisions for MVP

### **1. Start Local or Cloud?**
**Recommendation**: **Start local**
- Faster iteration
- Free (no cloud costs)
- Deploy to cloud Week 3 if needed

### **2. Manual Steps vs. Automated?**
**MVP**: Manual is OK for:
- ✅ Gumroad product upload (5 minutes)
- ✅ Social media posting (10 minutes)
- ✅ Seeding initial ideas (15 minutes)

**Must be automated**:
- ❌ Icon generation (this is the core!)
- ❌ Quality checking
- ❌ File packaging

### **3. Quality: Good Enough vs. Perfect?**
**MVP Standard**: **Good enough to sell**
- Icons don't need to be Dribbble-worthy
- They need to be consistent and useful
- $47 is mid-range pricing (not premium)
- First customer forgives rough edges

### **4. One Product vs. Multiple?**
**MVP**: **ONE product, done right**
- Prove the pipeline works end-to-end
- Learn from real market feedback
- Scale to multiple products Week 5+

---

## 🚀 Next Steps (Starting RIGHT NOW)

### **Today (Next 2 Hours)**:
```yaml
step_1:
  task: "Sign up for GCP account"
  time: "15 minutes"
  result: "$300 credits + always free tier"

step_2:
  task: "Clone agent-starter-pack repo"
  time: "5 minutes"
  result: "Have codebase locally"

step_3:
  task: "Set up Python virtual environment"
  time: "10 minutes"
  result: "Clean Python environment"

step_4:
  task: "Install core dependencies"
  time: "10 minutes"
  result: "Can run Python code"

step_5:
  task: "Get Anthropic API key"
  time: "10 minutes"
  result: "Can call Claude API"

step_6:
  task: "Test Claude API (hello world)"
  time: "20 minutes"
  result: "Verify API works"

total_time: "70 minutes to be up and running"
```

### **Tomorrow (Week 1, Days 2-7)**:
- Set up Docker Compose (PostgreSQL + Redis)
- Create database schema
- Build base Agent class
- Test end-to-end: Agent → Claude → Database

### **Week 2-3**:
- Build pipeline agents
- Generate first icon pack
- Launch on Gumroad

### **Week 4**:
- Track results
- Learn & iterate

---

## 🎉 The Moment of Truth

**4 weeks from now, we'll know**:
- ✅ Does the pipeline work? (Can AI create a sellable product?)
- ✅ Will people buy? (Does it generate revenue?)
- ✅ Is it profitable? (Revenue > costs?)
- ✅ Can we scale? (Launch product #2 faster?)

**If YES to all four**: You have an autonomous product factory. Scale it.

**If NO to some**: You have clear learnings on what to fix. Iterate.

**Either way**: You'll know more in 4 weeks than months of planning.

---

## 💪 Let's Get Building

**Ready to start with GCP signup and environment setup?**

Or do you want to discuss/adjust the MVP scope first?

**I'm here to help you build this thing, step by step.** 🚀
