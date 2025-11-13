-- Agent City Simulation Database Initialization
-- This script runs automatically when PostgreSQL container starts

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create schemas
CREATE SCHEMA IF NOT EXISTS identities;
CREATE SCHEMA IF NOT EXISTS geography;
CREATE SCHEMA IF NOT EXISTS agents;
CREATE SCHEMA IF NOT EXISTS trading;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA public TO agent_user;
GRANT ALL PRIVILEGES ON SCHEMA identities TO agent_user;
GRANT ALL PRIVILEGES ON SCHEMA geography TO agent_user;
GRANT ALL PRIVILEGES ON SCHEMA agents TO agent_user;
GRANT ALL PRIVILEGES ON SCHEMA trading TO agent_user;
GRANT ALL PRIVILEGES ON SCHEMA analytics TO agent_user;

-- =============================================================================
-- IDENTITIES SCHEMA - Agent identity information
-- =============================================================================

-- Identities table
CREATE TABLE IF NOT EXISTS identities.persons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    age INT GENERATED ALWAYS AS (EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))) STORED,
    gender VARCHAR(50),
    nationality VARCHAR(100),
    email VARCHAR(255),
    phone_number VARCHAR(50),
    ssn VARCHAR(50),  -- For US identities
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Addresses table
CREATE TABLE IF NOT EXISTS identities.addresses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES identities.persons(id) ON DELETE CASCADE,
    address_type VARCHAR(50),  -- home, work, etc.
    street_address VARCHAR(255),
    apartment VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100),
    location GEOGRAPHY(POINT, 4326),  -- PostGIS point for spatial queries
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Skills table
CREATE TABLE IF NOT EXISTS identities.skills (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES identities.persons(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    skill_category VARCHAR(100),  -- technical, soft, domain, etc.
    proficiency_level VARCHAR(50),  -- beginner, intermediate, advanced, expert
    years_experience INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employment history table
CREATE TABLE IF NOT EXISTS identities.employment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES identities.persons(id) ON DELETE CASCADE,
    company_name VARCHAR(200),
    job_title VARCHAR(200),
    industry VARCHAR(100),
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT false,
    salary_range VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Family relationships table
CREATE TABLE IF NOT EXISTS identities.family (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES identities.persons(id) ON DELETE CASCADE,
    related_person_id UUID REFERENCES identities.persons(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50),  -- spouse, child, parent, sibling, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT no_self_relation CHECK (person_id != related_person_id)
);

-- Financial profiles table
CREATE TABLE IF NOT EXISTS identities.financial_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES identities.persons(id) ON DELETE CASCADE,
    annual_income DECIMAL(12, 2),
    savings DECIMAL(12, 2),
    debt DECIMAL(12, 2),
    credit_score INT,
    risk_tolerance VARCHAR(50),  -- conservative, moderate, aggressive
    investment_experience VARCHAR(50),  -- none, beginner, intermediate, advanced
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- GEOGRAPHY SCHEMA - City simulation
-- =============================================================================

-- City configuration
CREATE TABLE IF NOT EXISTS geography.cities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    country VARCHAR(100),
    population INT,
    area_km2 DECIMAL(10, 2),
    boundary GEOGRAPHY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Neighborhoods
CREATE TABLE IF NOT EXISTS geography.neighborhoods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    city_id UUID REFERENCES geography.cities(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50),  -- residential, commercial, industrial, mixed
    population INT,
    median_income DECIMAL(12, 2),
    boundary GEOGRAPHY(POLYGON, 4326),
    center_point GEOGRAPHY(POINT, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Streets
CREATE TABLE IF NOT EXISTS geography.streets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    neighborhood_id UUID REFERENCES geography.neighborhoods(id) ON DELETE CASCADE,
    name VARCHAR(200),
    street_type VARCHAR(50),  -- avenue, street, road, boulevard, etc.
    geometry GEOGRAPHY(LINESTRING, 4326),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Points of interest
CREATE TABLE IF NOT EXISTS geography.points_of_interest (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    neighborhood_id UUID REFERENCES geography.neighborhoods(id) ON DELETE CASCADE,
    name VARCHAR(200),
    category VARCHAR(100),  -- office, restaurant, park, store, etc.
    location GEOGRAPHY(POINT, 4326),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- AGENTS SCHEMA - Agent runtime information
-- =============================================================================

-- Agents table
CREATE TABLE IF NOT EXISTS agents.agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id UUID REFERENCES identities.persons(id),
    agent_type VARCHAR(100),  -- researcher, builder, trader, etc.
    department VARCHAR(100),  -- rd, builders, stockbrokers
    status VARCHAR(50),  -- active, paused, stopped, error
    current_location GEOGRAPHY(POINT, 4326),
    memory JSONB,
    configuration JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_heartbeat TIMESTAMP
);

-- Agent events log
CREATE TABLE IF NOT EXISTS agents.events (
    id BIGSERIAL PRIMARY KEY,
    agent_id UUID REFERENCES agents.agents(id) ON DELETE CASCADE,
    event_type VARCHAR(100),
    event_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agent_events_agent_id ON agents.events(agent_id);
CREATE INDEX idx_agent_events_created_at ON agents.events(created_at);

-- Agent communication
CREATE TABLE IF NOT EXISTS agents.messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_agent_id UUID REFERENCES agents.agents(id) ON DELETE CASCADE,
    to_agent_id UUID REFERENCES agents.agents(id) ON DELETE CASCADE,
    message_type VARCHAR(100),
    message_body JSONB,
    read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_to_agent ON agents.messages(to_agent_id, read);

-- =============================================================================
-- TRADING SCHEMA - Stockbroker department data
-- =============================================================================

-- Portfolios
CREATE TABLE IF NOT EXISTS trading.portfolios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents.agents(id) ON DELETE CASCADE,
    initial_capital DECIMAL(12, 2) NOT NULL,
    current_value DECIMAL(12, 2),
    cash_balance DECIMAL(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Positions
CREATE TABLE IF NOT EXISTS trading.positions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID REFERENCES trading.portfolios(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    asset_type VARCHAR(50),  -- stock, etf, bond, etc.
    quantity DECIMAL(18, 8),
    average_price DECIMAL(12, 2),
    current_price DECIMAL(12, 2),
    market_value DECIMAL(12, 2),
    unrealized_pnl DECIMAL(12, 2),
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trades
CREATE TABLE IF NOT EXISTS trading.trades (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    portfolio_id UUID REFERENCES trading.portfolios(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents.agents(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,  -- buy, sell
    quantity DECIMAL(18, 8) NOT NULL,
    price DECIMAL(12, 2),
    total_value DECIMAL(12, 2),
    commission DECIMAL(12, 2),
    trading_mode VARCHAR(20),  -- paper, live
    external_order_id VARCHAR(100),
    status VARCHAR(50),  -- pending, filled, partial, cancelled, rejected
    strategy_name VARCHAR(100),
    reasoning TEXT,
    executed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trades_agent_id ON trading.trades(agent_id);
CREATE INDEX idx_trades_symbol ON trading.trades(symbol);
CREATE INDEX idx_trades_executed_at ON trading.trades(executed_at);

-- =============================================================================
-- ANALYTICS SCHEMA - Analysis and predictions
-- =============================================================================

-- Predictions
CREATE TABLE IF NOT EXISTS analytics.predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    predictor_agent_id UUID REFERENCES agents.agents(id),
    prediction_type VARCHAR(100),  -- market_movement, trend, demand, etc.
    subject VARCHAR(200),  -- What is being predicted
    prediction_data JSONB,
    confidence DECIMAL(5, 4),  -- 0.0000 to 1.0000
    reasoning TEXT,
    data_sources JSONB,
    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP,
    outcome JSONB,  -- Actual outcome (filled in later)
    accuracy_score DECIMAL(5, 4)  -- How accurate was it
);

CREATE INDEX idx_predictions_type ON analytics.predictions(prediction_type);
CREATE INDEX idx_predictions_confidence ON analytics.predictions(confidence);

-- Rankings
CREATE TABLE IF NOT EXISTS analytics.rankings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ranker_agent_id UUID REFERENCES agents.agents(id),
    ranking_type VARCHAR(100),  -- opportunity, idea, performance, etc.
    subject VARCHAR(200),
    score DECIMAL(10, 4),
    criteria JSONB,
    reasoning TEXT,
    ranked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP
);

CREATE INDEX idx_rankings_type ON analytics.rankings(ranking_type);
CREATE INDEX idx_rankings_score ON analytics.rankings(score);

-- Research findings (from R&D department)
CREATE TABLE IF NOT EXISTS analytics.research_findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    researcher_agent_id UUID REFERENCES agents.agents(id),
    research_type VARCHAR(100),  -- market, technology, consumer, etc.
    topic VARCHAR(200),
    findings JSONB,
    confidence DECIMAL(5, 4),
    data_sources JSONB,
    actionable_insights JSONB,
    shared_with VARCHAR[], -- Which departments received this
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_research_type ON analytics.research_findings(research_type);

-- =============================================================================
-- INDEXES for Performance
-- =============================================================================

-- Identities indexes
CREATE INDEX idx_persons_email ON identities.persons(email);
CREATE INDEX idx_persons_last_name ON identities.persons(last_name);
CREATE INDEX idx_addresses_person_id ON identities.addresses(person_id);
CREATE INDEX idx_addresses_location ON identities.addresses USING GIST(location);
CREATE INDEX idx_skills_person_id ON identities.skills(person_id);
CREATE INDEX idx_employment_person_id ON identities.employment(person_id);

-- Geography indexes
CREATE INDEX idx_neighborhoods_city_id ON geography.neighborhoods(city_id);
CREATE INDEX idx_neighborhoods_boundary ON geography.neighborhoods USING GIST(boundary);
CREATE INDEX idx_streets_neighborhood_id ON geography.streets(neighborhood_id);
CREATE INDEX idx_streets_geometry ON geography.streets USING GIST(geometry);
CREATE INDEX idx_poi_location ON geography.points_of_interest USING GIST(location);

-- Agents indexes
CREATE INDEX idx_agents_person_id ON agents.agents(person_id);
CREATE INDEX idx_agents_status ON agents.agents(status);
CREATE INDEX idx_agents_department ON agents.agents(department);
CREATE INDEX idx_agents_location ON agents.agents USING GIST(current_location);

-- =============================================================================
-- FUNCTIONS and TRIGGERS
-- =============================================================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update trigger to relevant tables
CREATE TRIGGER update_persons_updated_at BEFORE UPDATE ON identities.persons
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_financial_profiles_updated_at BEFORE UPDATE ON identities.financial_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents.agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_portfolios_updated_at BEFORE UPDATE ON trading.portfolios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_positions_updated_at BEFORE UPDATE ON trading.positions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant all permissions on all tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agent_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA identities TO agent_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA geography TO agent_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA agents TO agent_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA trading TO agent_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO agent_user;

GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA identities TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA geography TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA agents TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA trading TO agent_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO agent_user;

-- Done!
\echo 'Database initialization complete!'
