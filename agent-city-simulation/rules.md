# Project Rules and Principles

## Core Principles

### 1. NO MOCK DATA
- Every piece of data must be real, generated, or sourced from live APIs
- No hardcoded placeholder values
- No fake API responses
- No dummy data in production code
- Test environments can use controlled real data, but never obviously fake data

### 2. DO NOT LIE
- Agents must never fabricate information
- All predictions must be based on actual analysis, not random outputs
- System logs must be truthful
- Performance metrics must be accurate
- If data is unavailable, acknowledge it rather than inventing it

### 3. REAL CONSEQUENCES
- Stockbroker trades use real money and have real financial impact
- Failed predictions should inform learning, not be hidden
- System failures must be logged and addressed
- Performance metrics reflect actual outcomes, not aspirational goals

### 4. AUTONOMOUS OPERATION
- Agents must operate without constant human intervention
- Each department makes independent decisions
- Human oversight is for monitoring, not micromanaging
- System should handle errors gracefully without requiring manual fixes

### 5. LEARNING FROM FAILURE (Hydra Principle)
- Every failure is a learning opportunity
- System must log failures with context
- Adapt strategies based on what didn't work
- Come back stronger after setbacks
- Never repeat the same mistake twice

## Development Rules

### Code Quality
- Write production-grade code from day one
- Comprehensive error handling
- Extensive logging for debugging
- Type safety where applicable
- Clear documentation
- No "TODO: implement this later" shortcuts

### Testing
- Test with real API integrations (sandboxes where available)
- Load test with target concurrency (300 agents)
- Stress test failure scenarios
- Validate data integrity continuously
- No untested code in production

### Performance
- Optimize for 300+ concurrent operations
- Efficient resource usage (memory, CPU, API calls)
- Proper connection pooling and rate limiting
- Asynchronous operations where appropriate
- Monitor and profile regularly

### Security
- Secure API key management
- Never commit secrets to version control
- Encrypted data storage where appropriate
- Audit logs for sensitive operations
- Compliance with data protection regulations

## Financial Trading Rules

### Risk Management
- Maximum position size limits per trade
- Portfolio-level diversification requirements
- Daily loss limits (circuit breakers)
- Maximum capital allocation per agent
- Regular risk assessment and rebalancing

### Compliance
- Operate within legal and regulatory frameworks
- No market manipulation
- Proper record-keeping of all trades
- Transparent decision audit trails
- Regular compliance reviews

### Capital Protection
- Start with limited capital per agent
- Prove strategies in paper trading first
- Scale capital allocation based on proven performance
- Emergency shutdown mechanisms
- Regular strategy backtesting

## Agent Behavior Rules

### Realism
- Agents must behave like real people/organizations
- Decision-making should be rational but not perfect
- Include human-like considerations (risk aversion, biases, learning curves)
- Agents can make mistakes and learn from them
- Social interactions should feel natural

### Consistency
- Agent personalities and risk profiles remain stable
- Decision patterns should be traceable
- Memory and context persist across sessions
- No sudden unexplained behavior changes

### Ethics
- Agents operate within societal and legal norms
- No unethical trading practices
- Respect privacy and data protection
- Fair and unbiased ranking and evaluation
- Transparent decision-making processes

## Communication Rules

### Inter-Agent Communication
- Clear, structured message formats
- Traceable communication logs
- No message loss or duplication
- Appropriate authentication and authorization
- Rate limiting to prevent spam

### External Communication
- Rate limit API calls to respect service limits
- Handle API errors gracefully
- Implement exponential backoff for retries
- Cache where appropriate to reduce API load
- Monitor API costs

## Data Rules

### Data Quality
- Validate all incoming data
- Clean and normalize data before use
- Handle missing or corrupted data gracefully
- Regular data quality audits
- Clear data provenance tracking

### Data Privacy
- Respect API terms of service
- No unauthorized data scraping
- Proper attribution of data sources
- Comply with data retention policies
- Anonymize sensitive information where required

## Operational Rules

### Monitoring
- Real-time system health monitoring
- Alert on anomalies and errors
- Track key performance indicators
- Regular performance reviews
- Capacity planning based on metrics

### Maintenance
- Regular dependency updates
- Security patches applied promptly
- Database maintenance and optimization
- Log rotation and archival
- Disaster recovery procedures tested regularly

### Scaling
- Design for horizontal scalability
- No hardcoded limits that prevent growth
- Resource allocation based on demand
- Graceful degradation under load
- Clear scaling procedures documented

## Prohibited Practices

❌ Using placeholder or mock data in production
❌ Hardcoding configuration values
❌ Ignoring errors or exceptions
❌ Operating without proper monitoring
❌ Trading without risk management
❌ Making decisions without audit trails
❌ Deploying untested code
❌ Ignoring regulatory requirements
❌ Exposing API keys or secrets
❌ Creating agents that can't explain their decisions

## Mandatory Practices

✅ Comprehensive logging at all levels
✅ Real data from live sources
✅ Proper error handling and recovery
✅ Risk management on all trades
✅ Regular testing and validation
✅ Clear documentation
✅ Performance monitoring
✅ Security best practices
✅ Regulatory compliance
✅ Learning from failures
