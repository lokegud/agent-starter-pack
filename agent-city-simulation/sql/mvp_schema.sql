-- Agent City MVP Database Schema
-- Phase 1: Idea Factory (Scout Agents)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Scout Findings Table
-- Stores opportunities found by scout agents from various sources
CREATE TABLE IF NOT EXISTS scout_findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Source information
    source VARCHAR(50) NOT NULL,  -- 'reddit', 'producthunt', 'twitter', 'github'
    source_url TEXT,
    subreddit VARCHAR(100),  -- For Reddit posts

    -- Content
    title VARCHAR(500) NOT NULL,
    description TEXT,
    author VARCHAR(255),

    -- Engagement metrics
    upvotes INT DEFAULT 0,
    comments INT DEFAULT 0,
    views INT DEFAULT 0,

    -- AI Analysis
    opportunity_score DECIMAL(3,2),  -- 0.00 to 1.00
    category VARCHAR(100),
    keywords TEXT[],  -- Array of keywords
    ai_analysis TEXT,  -- Claude's analysis

    -- Scoring breakdown
    market_demand_score DECIMAL(3,2),
    feasibility_score DECIMAL(3,2),
    competition_score DECIMAL(3,2),
    revenue_potential_score DECIMAL(3,2),

    -- Status tracking
    status VARCHAR(20) DEFAULT 'new',  -- 'new', 'reviewed', 'approved', 'rejected', 'in_progress'

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    scout_agent_id VARCHAR(100)  -- Which agent found this
);

-- Scout Runs Table
-- Tracks each time scouts are executed
CREATE TABLE IF NOT EXISTS scout_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source VARCHAR(50) NOT NULL,
    scout_type VARCHAR(100),  -- 'news_hunter', 'community_listener', etc.

    findings_count INT DEFAULT 0,
    high_score_count INT DEFAULT 0,  -- Findings with score > 0.7

    status VARCHAR(20) DEFAULT 'running',  -- 'running', 'completed', 'failed'
    error_message TEXT,

    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    duration_seconds INT
);

-- Ideas Table (for approved opportunities)
-- Stores ideas that passed initial evaluation
CREATE TABLE IF NOT EXISTS ideas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    finding_id UUID REFERENCES scout_findings(id),

    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Evaluation Committee scores (Phase 2)
    evaluation_score DECIMAL(3,2),
    evaluation_votes JSONB,  -- Store individual expert votes

    source VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',  -- 'pending', 'approved', 'rejected', 'in_design', 'in_build'

    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Products Table (Phase 2+)
-- Stores products being built
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    idea_id UUID REFERENCES ideas(id),

    product_type VARCHAR(50) NOT NULL,  -- 'icon_pack', 'template', 'saas', etc.
    title VARCHAR(255) NOT NULL,
    description TEXT,

    status VARCHAR(20) DEFAULT 'designing',  -- 'designing', 'building', 'testing', 'launching', 'live', 'retired'

    -- File storage
    files JSONB,  -- {design_spec: 'path', assets: ['path1', 'path2'], package: 'path'}

    -- Marketplace info
    marketplace VARCHAR(50),  -- 'gumroad', 'creative_market', 'own_store'
    marketplace_url TEXT,
    price DECIMAL(10,2),

    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    launched_at TIMESTAMP
);

-- Outcomes Table (Phase 2+)
-- Tracks revenue and performance
CREATE TABLE IF NOT EXISTS outcomes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),

    -- Financial metrics
    revenue DECIMAL(10,2) DEFAULT 0,
    sales_count INT DEFAULT 0,

    -- Engagement metrics
    views INT DEFAULT 0,
    clicks INT DEFAULT 0,
    conversion_rate DECIMAL(5,4),  -- 0.0000 to 1.0000

    -- Feedback
    feedback TEXT,
    rating DECIMAL(3,2),

    metadata JSONB,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Agent Logs Table
-- Tracks all agent activity for debugging and learning
CREATE TABLE IF NOT EXISTS agent_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    agent_type VARCHAR(50),  -- 'scout', 'evaluator', 'designer', etc.
    agent_id VARCHAR(100),

    task VARCHAR(255),
    status VARCHAR(20),  -- 'started', 'completed', 'failed'

    input JSONB,
    output JSONB,
    error TEXT,

    -- Performance metrics
    tokens_used INT,
    cost_usd DECIMAL(10,6),
    duration_seconds INT,

    created_at TIMESTAMP DEFAULT NOW()
);

-- Source Credibility Table (for recursive learning)
-- Tracks which sources produce successful products
CREATE TABLE IF NOT EXISTS source_credibility (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source VARCHAR(50) NOT NULL,
    subreddit VARCHAR(100),  -- For Reddit

    -- Success metrics
    findings_count INT DEFAULT 0,
    approved_count INT DEFAULT 0,
    launched_count INT DEFAULT 0,
    revenue_generated DECIMAL(10,2) DEFAULT 0,

    -- Calculated score
    credibility_score DECIMAL(3,2) DEFAULT 0.50,  -- 0.00 to 1.00, starts at 0.50

    last_updated TIMESTAMP DEFAULT NOW(),

    UNIQUE(source, subreddit)
);

-- Agent Reputation Table (for recursive learning)
-- Tracks which agents make good decisions
CREATE TABLE IF NOT EXISTS agent_reputation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    agent_id VARCHAR(100) NOT NULL UNIQUE,
    agent_type VARCHAR(50),

    -- Performance metrics
    tasks_completed INT DEFAULT 0,
    tasks_successful INT DEFAULT 0,

    -- Outcomes
    products_contributed INT DEFAULT 0,
    revenue_generated DECIMAL(10,2) DEFAULT 0,

    -- Calculated score
    reputation_score DECIMAL(3,2) DEFAULT 0.50,  -- 0.00 to 1.00, starts at 0.50

    last_updated TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_scout_findings_source ON scout_findings(source);
CREATE INDEX idx_scout_findings_score ON scout_findings(opportunity_score DESC);
CREATE INDEX idx_scout_findings_status ON scout_findings(status);
CREATE INDEX idx_scout_findings_created ON scout_findings(created_at DESC);

CREATE INDEX idx_ideas_status ON ideas(status);
CREATE INDEX idx_ideas_score ON ideas(evaluation_score DESC);

CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_products_idea ON products(idea_id);

CREATE INDEX idx_outcomes_product ON outcomes(product_id);

CREATE INDEX idx_agent_logs_type ON agent_logs(agent_type);
CREATE INDEX idx_agent_logs_created ON agent_logs(created_at DESC);

CREATE INDEX idx_source_credibility_score ON source_credibility(credibility_score DESC);
CREATE INDEX idx_agent_reputation_score ON agent_reputation(reputation_score DESC);

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_scout_findings_updated_at BEFORE UPDATE ON scout_findings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ideas_updated_at BEFORE UPDATE ON ideas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
