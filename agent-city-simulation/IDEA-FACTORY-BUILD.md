# Idea Factory Build Plan - Let's Generate Ideas TODAY

## 🎯 Goal: Scout real opportunities, score them, store them in database

**Timeline**: 1-2 days to first working scouts
**Output**: Real ideas with scores in your database

---

## 📊 What We're Building

### **Idea Factory Components (Simplified for Now)**

```yaml
phase_1_today:
  scouts:
    - reddit_scout: "Scrape trending posts from relevant subreddits"
    - producthunt_scout: "Get today's top products + engagement"

  analysis:
    - claude_analyzer: "AI analyzes each finding for opportunity"
    - scorer: "0-1 score based on multiple factors"

  storage:
    - database: "Store all findings with metadata"
    - deduplication: "Don't store same idea twice"

phase_2_tomorrow:
  scouts:
    - twitter_scout: "Trending topics, viral threads"
    - github_scout: "Trending repos, tech innovations"

  enhancements:
    - viral_velocity: "Track how fast trends are growing"
    - sentiment_analysis: "Positive vs negative buzz"

phase_3_later:
  scouts:
    - news_scout: "HackerNews, TechCrunch, etc."
    - community_scout: "Discord, Slack communities"
```

**We'll start with Reddit + ProductHunt** (easiest, no auth required)

---

## 🏗️ Step-by-Step Build

### **STEP 1: Database Schema** (10 min)

Create table to store scout findings:

```bash
cat > agent-city-simulation/sql/idea_factory_schema.sql << 'EOF'
-- Idea Factory Database Schema

-- Scout findings table
CREATE TABLE IF NOT EXISTS scout_findings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Source info
    source VARCHAR(50) NOT NULL,  -- 'reddit', 'producthunt', 'twitter'
    source_url TEXT,
    source_id VARCHAR(255),  -- Original post/product ID

    -- Content
    title VARCHAR(500) NOT NULL,
    description TEXT,
    author VARCHAR(255),

    -- Metrics
    upvotes INT DEFAULT 0,
    comments INT DEFAULT 0,
    views INT DEFAULT 0,
    engagement_rate DECIMAL(5,4),

    -- Analysis
    opportunity_score DECIMAL(3,2),  -- 0.00 to 1.00
    category VARCHAR(100),
    keywords TEXT[],
    ai_analysis TEXT,

    -- Metadata
    found_at TIMESTAMP DEFAULT NOW(),
    scout_agent VARCHAR(100),
    raw_data JSONB,

    -- Tracking
    status VARCHAR(20) DEFAULT 'new',  -- new, reviewed, selected, rejected
    created_at TIMESTAMP DEFAULT NOW()
);

-- Prevent duplicates
CREATE UNIQUE INDEX idx_scout_findings_unique
ON scout_findings(source, source_id);

-- Query optimization
CREATE INDEX idx_scout_findings_score ON scout_findings(opportunity_score DESC);
CREATE INDEX idx_scout_findings_source ON scout_findings(source);
CREATE INDEX idx_scout_findings_status ON scout_findings(status);
CREATE INDEX idx_scout_findings_found_at ON scout_findings(found_at DESC);

-- Scout run history
CREATE TABLE IF NOT EXISTS scout_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scout_type VARCHAR(50) NOT NULL,
    findings_count INT DEFAULT 0,
    success BOOLEAN DEFAULT true,
    error_message TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
EOF

# Load schema
docker exec -i agent_city_db psql -U agent_user -d agent_city < agent-city-simulation/sql/idea_factory_schema.sql
```

---

### **STEP 2: Base Scout Agent** (20 min)

```bash
mkdir -p agent-city-simulation/core/scouts

cat > agent-city-simulation/core/scouts/base_scout.py << 'EOF'
"""Base Scout Agent for Idea Factory"""

import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
import asyncpg

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScout:
    """Base class for all scout agents"""

    def __init__(self, scout_type: str):
        self.scout_type = scout_type
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20241022"
        self.db_pool = None

    async def connect_db(self):
        """Connect to PostgreSQL"""
        if not self.db_pool:
            self.db_pool = await asyncpg.create_pool(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=int(os.getenv("POSTGRES_PORT", 5432)),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                database=os.getenv("POSTGRES_DB")
            )

    async def analyze_opportunity(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Claude to analyze if this finding is a good product opportunity
        """
        prompt = f"""Analyze this trending item for product opportunity potential:

Title: {finding['title']}
Description: {finding.get('description', 'N/A')}
Source: {finding['source']}
Engagement: {finding.get('upvotes', 0)} upvotes, {finding.get('comments', 0)} comments

Evaluate this for:
1. Market demand (are people actually looking for this?)
2. Monetization potential (could this make money?)
3. Complexity (how hard to build?)
4. Competition (is this oversaturated?)
5. Timing (is this trend growing or fading?)

Provide:
- Opportunity score (0.0 to 1.0)
- Category (icon pack, template, SaaS tool, etc.)
- 3-5 keywords
- 2-3 sentence analysis

Format as JSON:
{{
    "score": 0.75,
    "category": "productivity tool",
    "keywords": ["task management", "teams", "collaboration"],
    "analysis": "Strong demand for team productivity tools. Market is large but competitive. Could differentiate with AI features."
}}
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0.3,  # Lower temp for more consistent scoring
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse Claude's response
            import json
            result_text = response.content[0].text

            # Extract JSON from response
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            json_str = result_text[start:end]

            result = json.loads(json_str)
            return result

        except Exception as e:
            logger.error(f"Error analyzing opportunity: {e}")
            return {
                "score": 0.0,
                "category": "unknown",
                "keywords": [],
                "analysis": f"Error: {e}"
            }

    async def save_finding(self, finding: Dict[str, Any], analysis: Dict[str, Any]):
        """Save finding to database"""
        await self.connect_db()

        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO scout_findings (
                        source, source_url, source_id, title, description,
                        author, upvotes, comments, views,
                        opportunity_score, category, keywords, ai_analysis,
                        scout_agent, raw_data
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15
                    )
                    ON CONFLICT (source, source_id) DO NOTHING
                """,
                    finding['source'],
                    finding.get('url'),
                    finding.get('id'),
                    finding['title'],
                    finding.get('description'),
                    finding.get('author'),
                    finding.get('upvotes', 0),
                    finding.get('comments', 0),
                    finding.get('views', 0),
                    analysis['score'],
                    analysis['category'],
                    analysis['keywords'],
                    analysis['analysis'],
                    self.scout_type,
                    finding  # Store full raw data as JSONB
                )

            logger.info(f"✅ Saved: {finding['title'][:50]}... (score: {analysis['score']})")

        except Exception as e:
            logger.error(f"Error saving finding: {e}")

    async def scout(self):
        """Override this in subclasses to implement specific scouting logic"""
        raise NotImplementedError("Subclasses must implement scout()")

    async def run(self) -> int:
        """Run the scout, return number of findings"""
        logger.info(f"🔍 Starting {self.scout_type} scout...")

        # Log scout run
        await self.connect_db()
        async with self.db_pool.acquire() as conn:
            run_id = await conn.fetchval("""
                INSERT INTO scout_runs (scout_type, started_at)
                VALUES ($1, NOW())
                RETURNING id
            """, self.scout_type)

        findings_count = 0
        try:
            findings = await self.scout()

            for finding in findings:
                # Analyze opportunity
                analysis = await self.analyze_opportunity(finding)

                # Only save if score is decent (> 0.3)
                if analysis['score'] > 0.3:
                    await self.save_finding(finding, analysis)
                    findings_count += 1
                else:
                    logger.info(f"⏭️  Skipped (low score): {finding['title'][:50]}...")

            # Update scout run
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE scout_runs
                    SET findings_count = $1, success = true, completed_at = NOW()
                    WHERE id = $2
                """, findings_count, run_id)

            logger.info(f"✅ {self.scout_type} complete: {findings_count} opportunities found")
            return findings_count

        except Exception as e:
            logger.error(f"❌ Scout run failed: {e}")

            # Update scout run with error
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    UPDATE scout_runs
                    SET success = false, error_message = $1, completed_at = NOW()
                    WHERE id = $2
                """, str(e), run_id)

            return 0

        finally:
            if self.db_pool:
                await self.db_pool.close()
EOF
```

---

### **STEP 3: Reddit Scout** (30 min)

```bash
cat > agent-city-simulation/core/scouts/reddit_scout.py << 'EOF'
"""Reddit Scout - Finds trending posts from relevant subreddits"""

import httpx
from typing import List, Dict, Any
from .base_scout import BaseScout
import logging

logger = logging.getLogger(__name__)


class RedditScout(BaseScout):
    """Scouts Reddit for trending product opportunities"""

    # Subreddits to monitor
    TARGET_SUBREDDITS = [
        'SideProject',      # Side projects
        'EntrepreneurRideAlong',  # Entrepreneur stories
        'Entrepreneur',     # General entrepreneurship
        'startups',         # Startup discussions
        'SaaS',            # SaaS products
        'indiehackers',    # Indie hacker community
        'UI_Design',       # UI/UX design trends
        'webdev',          # Web development
        'productivity',    # Productivity tools
        'minimalism'       # Minimalist products (icon packs, templates)
    ]

    def __init__(self):
        super().__init__("reddit_scout")
        self.base_url = "https://www.reddit.com"

    async def scout(self) -> List[Dict[str, Any]]:
        """Scout Reddit for trending opportunities"""
        findings = []

        async with httpx.AsyncClient() as client:
            for subreddit in self.TARGET_SUBREDDITS:
                logger.info(f"  📍 Scouting r/{subreddit}...")

                try:
                    # Get hot posts from subreddit (no auth needed for public subs)
                    url = f"{self.base_url}/r/{subreddit}/hot.json?limit=25"
                    headers = {"User-Agent": "AgentCityScout/1.0"}

                    response = await client.get(url, headers=headers, timeout=10)
                    response.raise_for_status()

                    data = response.json()
                    posts = data.get('data', {}).get('children', [])

                    for post in posts:
                        post_data = post.get('data', {})

                        # Skip stickied/pinned posts
                        if post_data.get('stickied'):
                            continue

                        finding = {
                            'source': 'reddit',
                            'id': post_data.get('id'),
                            'url': f"https://reddit.com{post_data.get('permalink')}",
                            'title': post_data.get('title'),
                            'description': post_data.get('selftext', '')[:500],  # First 500 chars
                            'author': post_data.get('author'),
                            'upvotes': post_data.get('ups', 0),
                            'comments': post_data.get('num_comments', 0),
                            'subreddit': subreddit,
                            'created_utc': post_data.get('created_utc')
                        }

                        findings.append(finding)

                    logger.info(f"    Found {len(posts)} posts in r/{subreddit}")

                except Exception as e:
                    logger.error(f"    Error scouting r/{subreddit}: {e}")
                    continue

        logger.info(f"  Total Reddit findings: {len(findings)}")
        return findings
EOF
```

---

### **STEP 4: ProductHunt Scout** (30 min)

```bash
cat > agent-city-simulation/core/scouts/producthunt_scout.py << 'EOF'
"""ProductHunt Scout - Finds trending products"""

import httpx
from typing import List, Dict, Any
from .base_scout import BaseScout
import logging

logger = logging.getLogger(__name__)


class ProductHuntScout(BaseScout):
    """Scouts ProductHunt for trending products"""

    def __init__(self):
        super().__init__("producthunt_scout")
        # We'll use public feed (no API key needed for basic scraping)
        self.base_url = "https://www.producthunt.com"

    async def scout(self) -> List[Dict[str, Any]]:
        """Scout ProductHunt for trending products"""
        findings = []

        # Note: ProductHunt's official API requires OAuth
        # For MVP, we'll scrape the public "today" page
        # Later, we can add proper API integration

        async with httpx.AsyncClient() as client:
            try:
                logger.info("  📍 Scouting ProductHunt...")

                # This is simplified - in production, use their GraphQL API
                # For now, we'll use a workaround or manual seeding

                # TODO: Implement ProductHunt scraping or API integration
                # For MVP, you can manually add top ProductHunt products

                logger.info("  ⚠️  ProductHunt scout not fully implemented yet")
                logger.info("  💡 Tip: Manually seed ideas from producthunt.com/today")

            except Exception as e:
                logger.error(f"Error scouting ProductHunt: {e}")

        return findings
EOF
```

---

### **STEP 5: CLI Tool** (20 min)

```bash
cat > agent-city-simulation/cli/run_scouts.py << 'EOF'
#!/usr/bin/env python3
"""CLI to run scout agents and view findings"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.scouts.reddit_scout import RedditScout
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()


async def run_all_scouts():
    """Run all available scouts"""
    print("🚀 Starting Idea Factory scouts...\n")

    scouts = [
        RedditScout(),
        # Add more scouts here as we build them
    ]

    total_findings = 0
    for scout in scouts:
        count = await scout.run()
        total_findings += count
        print()

    print(f"✅ All scouts complete! Total findings: {total_findings}\n")

    # Show top findings
    await show_top_findings()


async def show_top_findings(limit: int = 10):
    """Show top-scored findings"""
    print(f"📊 Top {limit} Opportunities:\n")

    pool = await asyncpg.create_pool(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB")
    )

    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT
                title,
                source,
                opportunity_score,
                category,
                upvotes,
                comments,
                ai_analysis
            FROM scout_findings
            WHERE status = 'new'
            ORDER BY opportunity_score DESC
            LIMIT $1
        """, limit)

    for i, row in enumerate(rows, 1):
        print(f"{i}. [{row['source'].upper()}] {row['title'][:60]}...")
        print(f"   Score: {row['opportunity_score']:.2f} | Category: {row['category']}")
        print(f"   Engagement: {row['upvotes']} upvotes, {row['comments']} comments")
        print(f"   Analysis: {row['ai_analysis'][:100]}...")
        print()

    await pool.close()


async def main():
    """Main CLI entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "scout":
            await run_all_scouts()
        elif command == "top":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            await show_top_findings(limit)
        elif command == "stats":
            await show_stats()
        else:
            print(f"Unknown command: {command}")
            show_help()
    else:
        # Default: run scouts
        await run_all_scouts()


async def show_stats():
    """Show statistics about scout runs"""
    print("📈 Idea Factory Statistics:\n")

    pool = await asyncpg.create_pool(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", 5432)),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB")
    )

    async with pool.acquire() as conn:
        # Total findings
        total = await conn.fetchval("SELECT COUNT(*) FROM scout_findings")
        print(f"Total findings: {total}")

        # By source
        by_source = await conn.fetch("""
            SELECT source, COUNT(*) as count, AVG(opportunity_score) as avg_score
            FROM scout_findings
            GROUP BY source
            ORDER BY count DESC
        """)
        print("\nBy source:")
        for row in by_source:
            print(f"  {row['source']}: {row['count']} findings (avg score: {row['avg_score']:.2f})")

        # Top categories
        by_category = await conn.fetch("""
            SELECT category, COUNT(*) as count, AVG(opportunity_score) as avg_score
            FROM scout_findings
            GROUP BY category
            ORDER BY count DESC
            LIMIT 5
        """)
        print("\nTop categories:")
        for row in by_category:
            print(f"  {row['category']}: {row['count']} findings (avg score: {row['avg_score']:.2f})")

        # High-scoring opportunities
        high_score = await conn.fetchval("""
            SELECT COUNT(*) FROM scout_findings WHERE opportunity_score >= 0.7
        """)
        print(f"\nHigh-value opportunities (score >= 0.7): {high_score}")

    await pool.close()


def show_help():
    """Show CLI help"""
    print("""
Idea Factory CLI

Usage:
  python cli/run_scouts.py [command]

Commands:
  scout           Run all scouts and find new opportunities
  top [N]         Show top N opportunities (default: 10)
  stats           Show statistics about findings

Examples:
  python cli/run_scouts.py scout     # Run all scouts
  python cli/run_scouts.py top 20    # Show top 20 opportunities
  python cli/run_scouts.py stats     # Show statistics
""")


if __name__ == "__main__":
    asyncio.run(main())
EOF

chmod +x agent-city-simulation/cli/run_scouts.py
```

---

### **STEP 6: Install Dependencies** (5 min)

```bash
# Add to requirements
pip install httpx asyncpg

# Or update requirements.txt
cat >> agent-city-simulation/requirements.txt << 'EOF'
httpx>=0.25.0
asyncpg>=0.29.0
EOF

pip install -r agent-city-simulation/requirements.txt
```

---

## 🚀 **LET'S RUN IT!**

### **Test Reddit Scout**

```bash
# Make sure database is running
docker-compose ps

# Load the Idea Factory schema
docker exec -i agent_city_db psql -U agent_user -d agent_city < agent-city-simulation/sql/idea_factory_schema.sql

# Run the scouts!
cd agent-city-simulation
python cli/run_scouts.py scout
```

**Expected output**:
```
🚀 Starting Idea Factory scouts...

🔍 Starting reddit_scout scout...
  📍 Scouting r/SideProject...
    Found 25 posts in r/SideProject
  📍 Scouting r/Entrepreneur...
    Found 25 posts in r/Entrepreneur
  ...

✅ Saved: Built a productivity tracker in 2 weeks... (score: 0.78)
✅ Saved: Icon pack for startup founders... (score: 0.72)
⏭️  Skipped (low score): Random blog post...
...

✅ reddit_scout complete: 45 opportunities found

📊 Top 10 Opportunities:

1. [REDDIT] Minimalist icon pack for productivity apps trending...
   Score: 0.85 | Category: icon pack
   Engagement: 234 upvotes, 45 comments
   Analysis: Strong demand for minimalist design assets. Icon packs are proven sellers...

2. [REDDIT] Built an AI-powered recipe optimizer, 1k users in 2 weeks...
   Score: 0.78 | Category: SaaS tool
   Engagement: 187 upvotes, 38 comments
   Analysis: Recipe optimization is trending. Market size is large...

...
```

---

## 📊 **View Your Ideas**

```bash
# Show top 20 opportunities
python cli/run_scouts.py top 20

# Show statistics
python cli/run_scouts.py stats
```

---

## 🎯 **What You Have Now**

✅ **Working scouts** that find real opportunities
✅ **AI analysis** (Claude scores each one)
✅ **Database** storing all findings
✅ **CLI tool** to run and view results

**You're generating ideas autonomously!** 🎉

---

## 🔄 **Run Daily**

```bash
# Set up a cron job (Mac/Linux)
crontab -e

# Add this line to run scouts every day at 9 AM:
0 9 * * * cd /path/to/agent-starter-pack/agent-city-simulation && /path/to/venv/bin/python cli/run_scouts.py scout
```

---

## 📈 **Next Steps**

**Tomorrow**:
1. Add Twitter/X scout
2. Add GitHub trending scout
3. Improve scoring algorithm

**This Week**:
1. Pick highest-scoring idea
2. Build Designer agent to create specs
3. Build Builder agent to generate product

**But for NOW**: Run the scouts, see what ideas come back, and we'll pick the best one to build!

---

Want me to help you run the first scout session right now?
