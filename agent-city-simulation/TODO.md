# Agent City - Complete Build TODO List

**Last Updated**: 2025-11-15
**Status**: Ready to build
**Estimated Timeline**: 12-16 weeks to full system

---

## 📋 How to Use This List

- [ ] = Not started
- [X] = Completed
- Each job has a summary and estimated time
- Tasks are sequential within each job
- Some jobs can run in parallel

---

## JOB 1: INITIAL SETUP & PREREQUISITES
**Summary**: Get development environment ready, accounts created, infrastructure running
**Estimated Time**: 2-4 hours
**Prerequisites**: Computer, credit card for GCP verification, email

### Cloud & API Setup
- [ ] Sign up for Google Cloud Platform account
- [ ] Verify GCP account (enter credit card info)
- [ ] Confirm $300 free credits activated
- [ ] Enable Vertex AI API in GCP Console
- [ ] Enable Cloud Storage API in GCP Console
- [ ] Enable Compute Engine API in GCP Console
- [ ] Create GCP project and note project ID
- [ ] Sign up for Anthropic account at console.anthropic.com
- [ ] Create Anthropic API key
- [ ] Save Anthropic API key securely
- [ ] Test Anthropic API key with curl/Postman

### Local Development Environment
- [ ] Install Python 3.11+ on local machine
- [ ] Verify Python installation (python3 --version)
- [ ] Install Docker Desktop (Mac/Windows) or Docker Engine (Linux)
- [ ] Verify Docker installation (docker --version)
- [ ] Start Docker Desktop and confirm it's running
- [ ] Install Git if not already installed
- [ ] Verify Git installation (git --version)
- [ ] Clone agent-starter-pack repository
- [ ] Navigate to agent-starter-pack directory
- [ ] Create Python virtual environment (python3 -m venv venv)
- [ ] Activate virtual environment
- [ ] Upgrade pip (pip install --upgrade pip)
- [ ] Install core dependencies (anthropic, python-dotenv, pyyaml, httpx, asyncpg)
- [ ] Create .env file in project root
- [ ] Add ANTHROPIC_API_KEY to .env file
- [ ] Add GCP project ID to .env file
- [ ] Add database credentials to .env file
- [ ] Create .gitignore and add .env to it
- [ ] Test that .env loads correctly

### Infrastructure Setup
- [ ] Create docker-compose.yml file
- [ ] Configure PostgreSQL service in docker-compose
- [ ] Configure Redis service in docker-compose
- [ ] Start Docker services (docker-compose up -d)
- [ ] Verify PostgreSQL is running (docker-compose ps)
- [ ] Verify Redis is running (docker-compose ps)
- [ ] Test PostgreSQL connection
- [ ] Test Redis connection
- [ ] Create agent-city-simulation directory structure
- [ ] Create sql/ directory for database schemas
- [ ] Create core/ directory for core code
- [ ] Create cli/ directory for command-line tools
- [ ] Create config/ directory for configuration files

---

## JOB 2: DATABASE FOUNDATION
**Summary**: Create all database schemas and tables needed for the system
**Estimated Time**: 1-2 hours
**Prerequisites**: PostgreSQL running in Docker

### Core Database Schema
- [ ] Create mvp_schema.sql file
- [ ] Define ideas table (id, title, description, score, status, metadata)
- [ ] Define products table (id, idea_id, product_type, title, status, files)
- [ ] Define outcomes table (id, product_id, revenue, sales_count, views, feedback)
- [ ] Define agent_logs table (id, agent_type, task, status, input, output, error)
- [ ] Add indexes on ideas.status
- [ ] Add indexes on ideas.score
- [ ] Add indexes on products.status
- [ ] Add indexes on products.idea_id
- [ ] Add indexes on outcomes.product_id
- [ ] Add indexes on agent_logs.agent_type
- [ ] Add indexes on agent_logs.created_at
- [ ] Load mvp_schema.sql into database
- [ ] Verify all tables created correctly
- [ ] Test inserting sample data into each table
- [ ] Test querying data from each table

### Idea Factory Schema
- [ ] Create idea_factory_schema.sql file
- [ ] Define scout_findings table (source, title, description, metrics, scores)
- [ ] Add unique constraint on (source, source_id) to prevent duplicates
- [ ] Add indexes on scout_findings.opportunity_score
- [ ] Add indexes on scout_findings.source
- [ ] Add indexes on scout_findings.status
- [ ] Add indexes on scout_findings.found_at
- [ ] Define scout_runs table (scout_type, findings_count, success, timestamps)
- [ ] Load idea_factory_schema.sql into database
- [ ] Verify scout tables created correctly
- [ ] Test inserting sample scout finding
- [ ] Test querying scout findings by score

### Recursive Learning Schema
- [ ] Create learning_schema.sql file
- [ ] Define source_credibility table (source, weight, adjustment_history)
- [ ] Define agent_reputation table (agent_id, reputation_score, outcomes)
- [ ] Define learned_patterns table (pattern, confidence, sample_size)
- [ ] Define decision_lineage table (decision_id, source_chain, outcome)
- [ ] Add indexes for performance
- [ ] Load learning_schema.sql into database
- [ ] Verify learning tables created
- [ ] Test credibility tracking logic
- [ ] Test pattern storage and retrieval

---

## JOB 3: BASE AGENT FRAMEWORK
**Summary**: Build core agent classes that all other agents inherit from
**Estimated Time**: 3-4 hours
**Prerequisites**: Database setup, Anthropic API key

### Base Agent Class
- [ ] Create core/agents/ directory
- [ ] Create base_agent.py file
- [ ] Define BaseAgent class
- [ ] Add __init__ method (agent_type, personality)
- [ ] Add Anthropic client initialization
- [ ] Add think() method to call Claude API
- [ ] Add error handling in think() method
- [ ] Add logging functionality
- [ ] Add log_task() method
- [ ] Add database connection pooling
- [ ] Add async support (asyncio)
- [ ] Create test_agent.py to test BaseAgent
- [ ] Run test and verify Claude API works
- [ ] Add personality trait influence logic (basic)
- [ ] Document BaseAgent class with docstrings
- [ ] Create example usage in comments

### Configuration Management
- [ ] Create core/shared/config/ directory
- [ ] Create settings.py file
- [ ] Define Settings class using Pydantic
- [ ] Add database configuration properties
- [ ] Add API keys configuration
- [ ] Add environment-specific settings (dev, prod)
- [ ] Create config.yaml template
- [ ] Add anthropic model settings to config
- [ ] Add vertex AI settings to config
- [ ] Add department enable/disable flags
- [ ] Test loading configuration from YAML
- [ ] Test loading from environment variables
- [ ] Add configuration validation
- [ ] Document all configuration options

---

## JOB 4: IDEA FACTORY - SCOUT AGENTS
**Summary**: Build scouts that find opportunities from Reddit, ProductHunt, Twitter, GitHub
**Estimated Time**: 6-8 hours
**Prerequisites**: Base agent framework, database schema

### Base Scout Framework
- [ ] Create core/scouts/ directory
- [ ] Create base_scout.py file
- [ ] Define BaseScout class (inherits from BaseAgent)
- [ ] Add connect_db() method
- [ ] Add analyze_opportunity() method using Claude
- [ ] Add save_finding() method to database
- [ ] Add deduplication logic (check source + source_id)
- [ ] Add scout() abstract method (to be overridden)
- [ ] Add run() method (logs scout run, handles errors)
- [ ] Test BaseScout with dummy data
- [ ] Add retry logic for API failures
- [ ] Add rate limiting to prevent API abuse

### Reddit Scout
- [ ] Create reddit_scout.py file
- [ ] Define RedditScout class (inherits BaseScout)
- [ ] Add list of target subreddits (SideProject, Entrepreneur, SaaS, etc.)
- [ ] Implement scout() method to fetch Reddit JSON
- [ ] Add HTTP client using httpx
- [ ] Parse Reddit post data (title, description, upvotes, comments)
- [ ] Filter out stickied/pinned posts
- [ ] Handle rate limiting from Reddit
- [ ] Add error handling for network failures
- [ ] Test Reddit scout with live data
- [ ] Verify findings saved to database
- [ ] Add logging for each subreddit scouted

### ProductHunt Scout
- [ ] Create producthunt_scout.py file
- [ ] Research ProductHunt API or scraping approach
- [ ] Define ProductHuntScout class
- [ ] Implement authentication if using API
- [ ] Implement scout() method to fetch top products
- [ ] Parse product data (name, tagline, votes, comments)
- [ ] Add fallback to manual seeding if API unavailable
- [ ] Test ProductHunt scout
- [ ] Verify data quality
- [ ] Document API limitations

### Twitter/X Scout
- [ ] Create twitter_scout.py file
- [ ] Research Twitter API v2 requirements
- [ ] Get Twitter API credentials (or use scraping)
- [ ] Define TwitterScout class
- [ ] Implement trending topics search
- [ ] Implement viral thread detection
- [ ] Parse tweet data (text, engagement, author)
- [ ] Filter out noise and spam
- [ ] Test Twitter scout
- [ ] Handle API rate limits

### GitHub Scout
- [ ] Create github_scout.py file
- [ ] Define GitHubScout class
- [ ] Use GitHub trending page or API
- [ ] Fetch trending repositories
- [ ] Parse repo data (name, description, stars, language)
- [ ] Filter for relevant tech categories
- [ ] Test GitHub scout
- [ ] Verify findings useful for product ideas

### Scout CLI Tool
- [ ] Create cli/run_scouts.py file
- [ ] Add run_all_scouts() function
- [ ] Add show_top_findings() function
- [ ] Add show_stats() function
- [ ] Add command-line argument parsing
- [ ] Implement "scout" command to run all scouts
- [ ] Implement "top [N]" command to show top findings
- [ ] Implement "stats" command for statistics
- [ ] Add colored output for better UX
- [ ] Add progress indicators
- [ ] Test CLI with all commands
- [ ] Make script executable (chmod +x)
- [ ] Add help documentation

---

## JOB 5: EVALUATION COMMITTEE
**Summary**: Build AI expert panel that evaluates and scores ideas
**Estimated Time**: 4-6 hours
**Prerequisites**: Scout findings in database

### Expert Panel Framework
- [ ] Create core/evaluation/ directory
- [ ] Create expert_agent.py file
- [ ] Define ExpertAgent class (inherits BaseAgent)
- [ ] Add expert personality traits (analytical, risk_tolerance, etc.)
- [ ] Add evaluate_idea() method
- [ ] Add vote() method (YES/NO with reasoning)
- [ ] Create 11 expert agent instances with unique personalities
- [ ] Assign influence weights to each expert
- [ ] Document each expert's specialty and decision style

### Evaluation Process
- [ ] Create evaluation_committee.py file
- [ ] Define EvaluationCommittee class
- [ ] Add conduct_evaluation() method
- [ ] Implement individual expert evaluation phase
- [ ] Implement voting phase
- [ ] Implement debate phase (if vote is close)
- [ ] Calculate consensus level
- [ ] Require 6+ YES votes to pass (majority)
- [ ] Generate comprehensive dossier for passed ideas
- [ ] Save evaluation results to database
- [ ] Track which experts voted YES/NO

### Money Potential Scoring
- [ ] Create scoring_system.py file
- [ ] Define calculate_money_potential() function
- [ ] Factor in market size estimate
- [ ] Factor in competition level
- [ ] Factor in complexity (difficulty to build)
- [ ] Factor in monetization potential
- [ ] Factor in trend velocity (growing vs fading)
- [ ] Combine into 0.0-1.0 final score
- [ ] Test scoring with various scenarios
- [ ] Validate scores make intuitive sense

### Evaluation CLI Tool
- [ ] Create cli/evaluate_ideas.py file
- [ ] Add command to evaluate top N scout findings
- [ ] Add command to show evaluation results
- [ ] Add command to show approved ideas (score >= 0.50)
- [ ] Add command to re-evaluate specific idea
- [ ] Test evaluation CLI
- [ ] Document usage

---

## JOB 6: DESIGNERS DEPARTMENT
**Summary**: Create detailed technical blueprints from approved ideas
**Estimated Time**: 6-8 hours
**Prerequisites**: Approved ideas from Evaluation Committee

### Designer Agent Framework
- [ ] Create core/designers/ directory
- [ ] Create base_designer.py file
- [ ] Define BaseDesigner class
- [ ] Add create_blueprint() abstract method
- [ ] Add save_blueprint() method to database

### System Architect Agent
- [ ] Create system_architect.py file
- [ ] Define SystemArchitect class
- [ ] Add design_architecture() method
- [ ] Generate tech stack recommendations
- [ ] Create architecture decision records (ADRs)
- [ ] Estimate build complexity and timeline
- [ ] Factor in personality (risk_tolerance affects tech choices)
- [ ] Test with sample idea
- [ ] Verify output quality

### UI/UX Designer Agent
- [ ] Create ui_designer.py file
- [ ] Define UIDesigner class
- [ ] Add design_mockups() method using Claude
- [ ] Generate component specifications
- [ ] Define color palette and style guide
- [ ] Create user flow descriptions
- [ ] Generate accessibility requirements
- [ ] Test with icon pack idea
- [ ] Verify design specs are actionable

### Database Designer Agent
- [ ] Create database_designer.py file
- [ ] Define DatabaseDesigner class
- [ ] Add design_schema() method
- [ ] Generate SQL schema with tables, indexes
- [ ] Define relationships and constraints
- [ ] Plan caching strategy
- [ ] Test with sample SaaS idea
- [ ] Verify SQL is valid

### API Designer Agent
- [ ] Create api_designer.py file
- [ ] Define APIDesigner class
- [ ] Add design_api() method
- [ ] Generate endpoint specifications
- [ ] Define request/response schemas
- [ ] Add authentication/authorization design
- [ ] Add rate limiting design
- [ ] Generate OpenAPI spec
- [ ] Test with sample API idea

### Design Coordinator
- [ ] Create design_coordinator.py file
- [ ] Define DesignCoordinator class
- [ ] Add coordinate_design() method
- [ ] Assemble team based on idea complexity
- [ ] Coordinate design sessions
- [ ] Compile final blueprint package
- [ ] Generate handoff document for Builders
- [ ] Test end-to-end design flow

### Design CLI Tool
- [ ] Create cli/design_product.py file
- [ ] Add command to design specific idea
- [ ] Add command to show design progress
- [ ] Add command to view blueprints
- [ ] Test design CLI

---

## JOB 7: BUILDERS DEPARTMENT
**Summary**: Generate actual product files from blueprints
**Estimated Time**: 8-12 hours
**Prerequisites**: Design blueprints ready

### Builder Agent Framework
- [ ] Create core/builders/ directory
- [ ] Create base_builder.py file
- [ ] Define BaseBuilder class
- [ ] Add build() abstract method
- [ ] Add package_files() method
- [ ] Add upload_to_storage() method (GCP Cloud Storage)

### Icon Pack Builder
- [ ] Create icon_builder.py file
- [ ] Define IconBuilder class
- [ ] Add generate_icons() method using Vertex AI Imagen
- [ ] Set up Vertex AI client
- [ ] Generate prompt for each icon from design spec
- [ ] Call Vertex AI Imagen API for each icon
- [ ] Save PNG files locally
- [ ] Convert PNG to SVG (using cairosvg or potrace)
- [ ] Organize files by size (512x512, 1024x1024, etc.)
- [ ] Create ZIP package of all icons
- [ ] Test with sample icon pack design
- [ ] Verify image quality

### Template Builder
- [ ] Create template_builder.py file
- [ ] Define TemplateBuilder class
- [ ] Add generate_template() method
- [ ] Support different template types (Notion, spreadsheet, Figma)
- [ ] Generate template structure from blueprint
- [ ] Save template files in appropriate formats
- [ ] Package templates for distribution
- [ ] Test with sample template design

### Code Builder (for SaaS products)
- [ ] Create code_builder.py file
- [ ] Define CodeBuilder class
- [ ] Add generate_code() method using Claude
- [ ] Generate frontend code (React, HTML/CSS)
- [ ] Generate backend code (Python, Node.js)
- [ ] Create project structure
- [ ] Generate configuration files
- [ ] Package code for deployment
- [ ] Test with simple SaaS idea
- [ ] Verify code quality

### Build Coordinator
- [ ] Create build_coordinator.py file
- [ ] Define BuildCoordinator class
- [ ] Add coordinate_build() method
- [ ] Assign builders based on product type
- [ ] Monitor build progress
- [ ] Handle build failures and retries
- [ ] Generate build report
- [ ] Test build coordination

### Build CLI Tool
- [ ] Create cli/build_product.py file
- [ ] Add command to build specific blueprint
- [ ] Add command to show build status
- [ ] Add command to download built products
- [ ] Test build CLI

---

## JOB 8: TESTERS DEPARTMENT
**Summary**: Quality assurance and certification before launch
**Estimated Time**: 6-8 hours
**Prerequisites**: Built products ready for testing

### QA Engineer Agent
- [ ] Create core/testers/ directory
- [ ] Create qa_engineer.py file
- [ ] Define QAEngineer class
- [ ] Add test_functionality() method
- [ ] Add visual_consistency_check() for icon packs
- [ ] Add file_validation() (formats, sizes, naming)
- [ ] Add usability_test() for templates
- [ ] Generate quality report
- [ ] Assign PASS/FAIL status
- [ ] Test QA agent with sample product

### Security Auditor Agent
- [ ] Create security_auditor.py file
- [ ] Define SecurityAuditor class
- [ ] Add scan_vulnerabilities() method
- [ ] Check for common security issues
- [ ] Validate input handling (if applicable)
- [ ] Generate security report
- [ ] Block if critical vulnerabilities found
- [ ] Test with various product types

### Performance Tester Agent
- [ ] Create performance_tester.py file
- [ ] Define PerformanceTester class
- [ ] Add test_load() method for digital products
- [ ] Test file sizes (ensure not too large)
- [ ] Test load times (for web products)
- [ ] Generate performance report
- [ ] Test performance tester

### Test Coordinator
- [ ] Create test_coordinator.py file
- [ ] Define TestCoordinator class
- [ ] Add coordinate_testing() method
- [ ] Run all required tests based on product type
- [ ] Collect test results
- [ ] Generate certification report
- [ ] Decide GO/NO-GO for launch
- [ ] Send back to Builders if FAIL
- [ ] Test coordination logic

### Test CLI Tool
- [ ] Create cli/test_product.py file
- [ ] Add command to test specific product
- [ ] Add command to show test results
- [ ] Add command to view certification reports
- [ ] Test CLI

---

## JOB 9: SALESMEN DEPARTMENT
**Summary**: Launch products to market and drive user acquisition
**Estimated Time**: 4-6 hours
**Prerequisites**: Tested products ready for launch

### Marketing Agent
- [ ] Create core/salesmen/ directory
- [ ] Create marketing_agent.py file
- [ ] Define MarketingAgent class
- [ ] Add create_product_description() method using Claude
- [ ] Add create_preview_images() method
- [ ] Add generate_seo_keywords() method
- [ ] Add write_social_posts() method
- [ ] Test marketing agent with sample product
- [ ] Verify copy quality

### Launch Specialist Agent
- [ ] Create launch_specialist.py file
- [ ] Define LaunchSpecialist class
- [ ] Add create_gumroad_listing() method (manual for MVP)
- [ ] Add prepare_launch_package() method
- [ ] Generate launch checklist
- [ ] Document launch process
- [ ] Test launch preparation

### Customer Success Agent
- [ ] Create customer_success.py file
- [ ] Define CustomerSuccess class
- [ ] Add collect_feedback() method
- [ ] Add track_metrics() method (views, sales, ratings)
- [ ] Add respond_to_reviews() method (draft responses)
- [ ] Test customer success agent

### Sales Coordinator
- [ ] Create sales_coordinator.py file
- [ ] Define SalesCoordinator class
- [ ] Add coordinate_launch() method
- [ ] Manage launch timeline
- [ ] Track launch outcomes
- [ ] Generate launch report
- [ ] Test sales coordination

### Sales CLI Tool
- [ ] Create cli/launch_product.py file
- [ ] Add command to prepare launch package
- [ ] Add command to show launch checklist
- [ ] Add command to track sales metrics
- [ ] Test sales CLI

---

## JOB 10: OUTCOME TRACKING & RECURSIVE LEARNING
**Summary**: Learn from every product outcome to improve the system
**Estimated Time**: 6-8 hours
**Prerequisites**: Products launched, outcomes tracked

### Outcome Tracker
- [ ] Create core/learning/ directory
- [ ] Create outcome_tracker.py file
- [ ] Define OutcomeTracker class
- [ ] Add track_product_outcome() method
- [ ] Collect revenue, sales count, views, feedback
- [ ] Classify outcome (success, moderate, failure)
- [ ] Save to outcomes table
- [ ] Test outcome tracking

### Source Credibility Updater
- [ ] Create source_credibility.py file
- [ ] Define SourceCredibility class
- [ ] Add update_source_weight() method
- [ ] Boost sources that led to successful products
- [ ] Reduce sources that led to failures
- [ ] Track adjustment history
- [ ] Test credibility updates

### Agent Reputation Tracker
- [ ] Create agent_reputation.py file
- [ ] Define AgentReputation class
- [ ] Add update_agent_reputation() method
- [ ] Track performance by agent type and individual
- [ ] Correlate agent work with product outcomes
- [ ] Adjust agent assignments based on reputation
- [ ] Test reputation tracking

### Pattern Learner
- [ ] Create pattern_learner.py file
- [ ] Define PatternLearner class
- [ ] Add learn_pattern() method
- [ ] Identify successful patterns (e.g., "ProductHunt launches work well")
- [ ] Build confidence scores based on sample size
- [ ] Store patterns in database
- [ ] Apply patterns to future decisions
- [ ] Test pattern learning

### Learning CLI Tool
- [ ] Create cli/view_learning.py file
- [ ] Add command to show source credibility rankings
- [ ] Add command to show agent reputation leaderboard
- [ ] Add command to show learned patterns
- [ ] Add command to show decision lineage for a product
- [ ] Test learning CLI

---

## JOB 11: DEPARTMENT OF GOOD TASTE
**Summary**: Quality reviewers that provide feedback at any stage
**Estimated Time**: 4-6 hours
**Prerequisites**: Other departments functional

### Design Critic Agent
- [ ] Create core/good_taste/ directory
- [ ] Create design_critic.py file
- [ ] Define DesignCritic class
- [ ] Add review_design() method
- [ ] Rate visual appeal, UX, accessibility, brand consistency
- [ ] Provide specific feedback and suggestions
- [ ] Assign verdict (APPROVED/APPROVED WITH REVISIONS/REJECTED)
- [ ] Test design critic

### Code Aesthete Agent
- [ ] Create code_aesthete.py file
- [ ] Define CodeAesthete class
- [ ] Add review_architecture() method
- [ ] Review for elegance, simplicity, maintainability
- [ ] Suggest improvements
- [ ] Test code aesthete

### Copy Editor Agent
- [ ] Create copy_editor.py file
- [ ] Define CopyEditor class
- [ ] Add review_copy() method
- [ ] Check clarity, tone, grammar
- [ ] Suggest improvements to marketing copy
- [ ] Test copy editor

### Good Taste Coordinator
- [ ] Create taste_coordinator.py file
- [ ] Define TasteCoordinator class
- [ ] Add request_review() method
- [ ] Route reviews to appropriate critic
- [ ] Track feedback acceptance rate
- [ ] Adjust reviewer reputation based on outcomes
- [ ] Test coordination

### Good Taste CLI Tool
- [ ] Create cli/request_review.py file
- [ ] Add command to request review of any artifact
- [ ] Add command to show review history
- [ ] Add command to show reviewer reputation
- [ ] Test CLI

---

## JOB 12: FULL PIPELINE INTEGRATION
**Summary**: Connect all departments into one automated flow
**Estimated Time**: 8-12 hours
**Prerequisites**: All departments built individually

### Pipeline Orchestrator
- [ ] Create core/pipeline/ directory
- [ ] Create pipeline_orchestrator.py file
- [ ] Define PipelineOrchestrator class
- [ ] Add run_full_pipeline() method
- [ ] Coordinate: Scout → Evaluate → Design → Build → Test → Launch
- [ ] Handle state transitions between stages
- [ ] Add error handling and retry logic
- [ ] Add pipeline status tracking
- [ ] Test full pipeline with one idea

### State Machine
- [ ] Create state_machine.py file
- [ ] Define ProductState enum (scouted, evaluated, designed, built, tested, launched)
- [ ] Add transition rules
- [ ] Validate state transitions
- [ ] Log all state changes
- [ ] Test state machine

### Event System
- [ ] Create event_bus.py file
- [ ] Define EventBus class
- [ ] Add publish() and subscribe() methods
- [ ] Allow departments to emit events (e.g., "build_complete")
- [ ] Other departments can react to events
- [ ] Test event system

### Full Pipeline CLI Tool
- [ ] Create cli/run_pipeline.py file
- [ ] Add command to run full pipeline
- [ ] Add command to show pipeline status for all products
- [ ] Add command to pause/resume pipeline
- [ ] Add command to show pipeline metrics
- [ ] Test pipeline CLI

---

## JOB 13: MONITORING & OBSERVABILITY
**Summary**: Track system health, performance, and outcomes
**Estimated Time**: 4-6 hours
**Prerequisites**: Pipeline running

### Logging System
- [ ] Set up structured logging (JSON format)
- [ ] Log all agent actions with timestamps
- [ ] Log API calls (Claude, Vertex AI)
- [ ] Log errors with full stack traces
- [ ] Configure log levels (DEBUG, INFO, WARN, ERROR)
- [ ] Write logs to files and stdout
- [ ] Test logging across all components

### Metrics Collector
- [ ] Create core/monitoring/ directory
- [ ] Create metrics_collector.py file
- [ ] Track ideas generated per day
- [ ] Track ideas approved per day
- [ ] Track products launched per day
- [ ] Track revenue per product
- [ ] Track API costs (Claude, Vertex AI)
- [ ] Track pipeline duration (idea to launch)
- [ ] Save metrics to database

### Dashboard (CLI-based)
- [ ] Create cli/dashboard.py file
- [ ] Show system overview (ideas, products, revenue)
- [ ] Show department status (active, idle, errors)
- [ ] Show recent activity log
- [ ] Show top performing products
- [ ] Show API usage and costs
- [ ] Refresh automatically or on command
- [ ] Test dashboard

### Alerting
- [ ] Create alerting.py file
- [ ] Alert on pipeline failures
- [ ] Alert on API errors
- [ ] Alert on cost overruns
- [ ] Alert on product launches
- [ ] Alert on first sale
- [ ] Send alerts via stdout (email/SMS later)
- [ ] Test alerting

---

## JOB 14: BUSINESS SETUP
**Summary**: Legal, financial, and operational setup for the business
**Estimated Time**: 4-8 hours (spread over days)
**Prerequisites**: None (can be done in parallel)

### Banking Setup
- [ ] Research business bank options (Relay, Novo, Mercury)
- [ ] Choose bank (Recommendation: Relay for free + 20 accounts)
- [ ] Sign up for business bank account
- [ ] Complete bank verification
- [ ] Set up multiple checking accounts (operating, taxes, products)
- [ ] Connect bank to accounting software

### Payment Processing
- [ ] Sign up for Gumroad account
- [ ] Complete Gumroad profile
- [ ] Connect Gumroad to bank account
- [ ] Sign up for Stripe account (for future SaaS products)
- [ ] Complete Stripe verification
- [ ] Test payment processing (sandbox mode)

### Business Formation (Optional, Recommended)
- [ ] Decide on business structure (sole prop vs LLC)
- [ ] Choose business name
- [ ] Check name availability in your state
- [ ] File LLC paperwork (or use Northwest Registered Agent)
- [ ] Get EIN from IRS (takes 5 minutes online)
- [ ] Open business bank account with LLC documents
- [ ] Set up bookkeeping software (Wave free or QuickBooks)

### Accounting Setup
- [ ] Choose accounting software (Wave or QuickBooks)
- [ ] Set up chart of accounts
- [ ] Connect bank account to accounting software
- [ ] Set up automatic expense categorization
- [ ] Create tax savings account (30% of revenue auto-transfer)
- [ ] Document write-offs (software, hardware, internet, etc.)
- [ ] Set up quarterly estimated tax payment reminders

---

## JOB 15: GRANT APPLICATIONS
**Summary**: Apply for funding to accelerate development
**Estimated Time**: 8-12 hours (spread over weeks)
**Prerequisites**: Business setup, working demo

### GCP Startup Program
- [ ] Create simple company website or landing page
- [ ] Get company email domain (yourcompany.com)
- [ ] Set up company email (yourname@yourcompany.com)
- [ ] Apply for GCP Startup Program (Start Tier: $2k credits)
- [ ] Submit application
- [ ] Wait for approval (1-2 weeks)
- [ ] If approved, activate credits

### Goose Grant Program
- [ ] Review Goose grant requirements (building on their platform)
- [ ] Assess if Agent City fits their criteria
- [ ] Draft grant proposal (project description, goals, timeline)
- [ ] Explain how Agent City uses autonomous agents
- [ ] Highlight multi-modal, self-improving aspects
- [ ] Submit application
- [ ] Follow up if needed

### Other Grants
- [ ] Research SBIR/STTR grants (NSF, DOE, NASA)
- [ ] Assess eligibility (small business, R&D focus)
- [ ] Decide if worth time investment (competitive, lengthy)
- [ ] If pursuing, draft detailed proposal
- [ ] Submit before deadlines

---

## JOB 16: MVP LAUNCH
**Summary**: Launch first product end-to-end to prove concept
**Estimated Time**: 1 week focused effort
**Prerequisites**: Full pipeline built and tested

### First Product Selection
- [ ] Run scouts to generate 50+ ideas
- [ ] Review top 10 highest-scoring ideas
- [ ] Manually select best idea (simple, proven market)
- [ ] Verify idea type is icon pack or template (easiest first product)
- [ ] Confirm idea passed Evaluation Committee (score >= 0.50)

### Full Pipeline Run
- [ ] Run Designers on selected idea
- [ ] Review design blueprint for quality
- [ ] Run Builders to generate product files
- [ ] Verify files generated correctly (50 icons or template)
- [ ] Run Testers to certify quality
- [ ] Review test results, fix any issues
- [ ] Run Salesmen to prepare launch
- [ ] Review marketing copy and preview images

### Manual Launch (for MVP)
- [ ] Create Gumroad product listing manually
- [ ] Upload product files (ZIP of icons or template)
- [ ] Add product title and description (from Salesmen)
- [ ] Upload preview images
- [ ] Set price ($47 for icon pack, $20-50 for template)
- [ ] Publish product on Gumroad
- [ ] Get product URL

### Marketing Push
- [ ] Post on Twitter/X with product link
- [ ] Post on Reddit (r/SideProject, r/UI_Design, etc.)
- [ ] Submit to ProductHunt (optional but recommended)
- [ ] Share in relevant Discord/Slack communities
- [ ] Email any existing contacts/followers
- [ ] Monitor initial reactions and traffic

### First Week Monitoring
- [ ] Check Gumroad analytics daily (views, sales)
- [ ] Track social media engagement
- [ ] Collect user feedback/comments
- [ ] Respond to questions and reviews
- [ ] Document lessons learned
- [ ] Record first sale (if achieved!)
- [ ] Celebrate first revenue (even if $1!)

---

## JOB 17: POST-LAUNCH LEARNING
**Summary**: Analyze first product outcome and improve system
**Estimated Time**: 4-6 hours
**Prerequisites**: Product launched, 1-2 weeks of data

### Outcome Analysis
- [ ] Collect final Week 1 metrics (revenue, sales, views, feedback)
- [ ] Record outcome in database (outcomes table)
- [ ] Classify outcome (success if $1+ revenue, moderate if 100+ views, failure otherwise)
- [ ] Analyze what worked and what didn't
- [ ] Document specific issues found

### System Updates
- [ ] Update source credibility based on outcome
- [ ] Update agent reputations based on quality of work
- [ ] Store learned patterns (e.g., "Icon packs from Reddit r/UI_Design sell well")
- [ ] Identify pipeline bottlenecks or failures
- [ ] Fix critical bugs found during launch
- [ ] Improve prompts that produced low-quality output

### Decision Point
- [ ] Decide: Did MVP prove the concept works?
- [ ] If YES: Plan to scale (launch product #2, #3, etc.)
- [ ] If NO: Identify what to fix and iterate
- [ ] Document decision and reasoning

---

## JOB 18: SCALE TO MULTIPLE PRODUCTS
**Summary**: Launch 2nd, 3rd, 4th products to test scaling
**Estimated Time**: Ongoing (2-4 weeks)
**Prerequisites**: First product successful or lessons learned

### Product #2
- [ ] Select 2nd highest-scoring idea from database
- [ ] Run through full pipeline (should be faster now)
- [ ] Launch on Gumroad
- [ ] Market on different channels than product #1
- [ ] Track outcomes
- [ ] Compare performance to product #1

### Product #3
- [ ] Select 3rd idea (try different product type - template instead of icons)
- [ ] Run pipeline
- [ ] Launch and market
- [ ] Track outcomes
- [ ] Analyze which product types perform better

### Product #4-10
- [ ] Repeat for 4th-10th products
- [ ] Vary product types (icons, templates, maybe simple SaaS)
- [ ] Vary marketing channels
- [ ] Test different price points
- [ ] Build portfolio of products
- [ ] Track cumulative revenue

### Pipeline Optimization
- [ ] Identify most time-consuming steps
- [ ] Automate any remaining manual steps
- [ ] Improve quality of AI-generated outputs
- [ ] Reduce API costs where possible
- [ ] Increase pipeline speed (goal: 1 product per week)

---

## JOB 19: AUTOMATION IMPROVEMENTS
**Summary**: Reduce manual intervention, increase autonomy
**Estimated Time**: 8-12 hours
**Prerequisites**: Multiple products launched successfully

### Automated Gumroad Integration
- [ ] Research Gumroad API capabilities
- [ ] Create Gumroad API integration
- [ ] Automate product creation on Gumroad
- [ ] Automate file uploads
- [ ] Automate description and preview image upload
- [ ] Test automated listing creation
- [ ] Deploy automation

### Automated Marketing
- [ ] Create Twitter API integration
- [ ] Automate tweet posting for new products
- [ ] Create Reddit API integration (or use scheduler)
- [ ] Automate Reddit posts to relevant subreddits
- [ ] Add buffer to avoid spam flags
- [ ] Test automated marketing
- [ ] Monitor for account bans/restrictions

### Scheduled Scout Runs
- [ ] Set up cron jobs or scheduler
- [ ] Run scouts daily at 9 AM
- [ ] Run evaluation automatically on new findings
- [ ] Alert when high-scoring ideas found
- [ ] Test scheduled runs
- [ ] Monitor for failures

---

## JOB 20: ADVANCED DEPARTMENTS (OPTIONAL)
**Summary**: Add Lawyers, Stockbrokers, and advanced features when ready
**Estimated Time**: 12-16 hours
**Prerequisites**: $5k+ revenue or 1,000+ users

### Lawyers & Compliance Department
- [ ] Define when to activate (1,000+ users or $10k+ revenue)
- [ ] Create privacy lawyer agent (GDPR, CCPA review)
- [ ] Create terms & conditions agent
- [ ] Add automated compliance checks
- [ ] Generate required legal documents
- [ ] Test lawyers department
- [ ] Deploy when threshold met

### Stockbrokers Department
- [ ] Define activation trigger ($5k+ revenue)
- [ ] Set up Alpaca API for paper trading
- [ ] Create trader agents (trend follower, mean reversion, etc.)
- [ ] Implement risk management (position limits, stop losses)
- [ ] Test paper trading for 30 days
- [ ] If successful, activate live trading with $1k-5k
- [ ] Monitor trading performance

### Meta-Orchestrator
- [ ] Create meta_orchestrator.py file
- [ ] Define MetaOrchestrator agent
- [ ] Add monitor_all_metrics() method
- [ ] Add recommend_optimizations() method
- [ ] Add auto_tune_parameters() method (with approval)
- [ ] Test meta-orchestrator
- [ ] Deploy with monitoring-only mode first

---

## JOB 21: PRODUCTION DEPLOYMENT
**Summary**: Deploy to GCP for 24/7 operation
**Estimated Time**: 8-12 hours
**Prerequisites**: System working well locally

### GCP Infrastructure
- [ ] Create GCP Cloud SQL instance (PostgreSQL)
- [ ] Migrate database schema to Cloud SQL
- [ ] Create GCP Memorystore instance (Redis)
- [ ] Create GCP Cloud Storage bucket for files
- [ ] Set up VPC and networking
- [ ] Configure firewall rules

### Application Deployment
- [ ] Containerize application (create Dockerfile)
- [ ] Build Docker image
- [ ] Push image to Google Container Registry
- [ ] Deploy to Cloud Run (or Compute Engine)
- [ ] Configure environment variables
- [ ] Set up Cloud Scheduler for cron jobs
- [ ] Test deployment

### Monitoring in Production
- [ ] Set up Cloud Logging
- [ ] Set up Cloud Monitoring
- [ ] Create alerts for errors
- [ ] Create alerts for cost overruns
- [ ] Set up uptime checks
- [ ] Test alerts

### Continuous Deployment
- [ ] Set up GitHub Actions or Cloud Build
- [ ] Create CI/CD pipeline
- [ ] Automate testing on push
- [ ] Automate deployment on merge to main
- [ ] Test CI/CD pipeline

---

## JOB 22: DOCUMENTATION & HANDOFF
**Summary**: Document everything for future reference or handoff
**Estimated Time**: 4-6 hours
**Prerequisites**: System fully functional

### Technical Documentation
- [ ] Document all agent classes and their purpose
- [ ] Document database schema with ERD diagrams
- [ ] Document API integrations (Claude, Vertex AI, Gumroad, etc.)
- [ ] Document configuration options
- [ ] Document deployment process
- [ ] Create troubleshooting guide

### User Documentation
- [ ] Create user guide for running scouts
- [ ] Create user guide for launching products
- [ ] Create user guide for monitoring outcomes
- [ ] Document common issues and solutions

### Business Documentation
- [ ] Document revenue and growth over time
- [ ] Document lessons learned
- [ ] Document successful vs unsuccessful product types
- [ ] Document best marketing channels
- [ ] Create playbook for future products

---

## 📊 PROGRESS TRACKING

**How to track progress:**
```bash
# Count completed tasks
grep -c "^- \[X\]" TODO.md

# Count total tasks
grep -c "^- \[" TODO.md

# Calculate percentage
# completed / total * 100
```

**Milestones:**
- [ ] Job 1-3 Complete: Foundation ready (Database + Agents)
- [ ] Job 4-5 Complete: Ideas being generated and evaluated
- [ ] Job 6-9 Complete: Full pipeline functional
- [ ] Job 16 Complete: First product launched (MVP COMPLETE!)
- [ ] Job 18 Complete: 10 products launched (SCALING)
- [ ] Job 21 Complete: Running 24/7 in cloud (PRODUCTION)

---

## 🎯 CURRENT FOCUS

**Start here:** Job 1 (Initial Setup)
**Next:** Job 2 (Database Foundation)
**Then:** Job 3 (Base Agent Framework)

**First major milestone:** Job 4 complete (Idea Factory working)

---

**Last Updated**: 2025-11-15
**Status**: Ready to execute
**Estimated Total Time**: 100-150 hours (spread over 12-16 weeks)

**LET'S BUILD THIS! 🚀**
