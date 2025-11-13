# Stockbrokers Department - The Trading Floor
*"Where market intelligence becomes real trades with real capital."*

## 🎯 Core Concept

The Stockbrokers Department manages **real capital** through **actual trading** on financial markets. This is NOT paper trading or simulation - these are real trades with real money, real gains, and real losses.

**Capital Sources**:
1. **Bootstrap Capital**: Initial funding ($5,000 - $50,000) provided to start trading
2. **Builder Revenue**: Profits from successful products built by Builder Department
3. **Trading Profits**: Reinvested gains from successful trades

**Trading Universe**:
- **Stocks**: US equities via Alpaca API
- **Options**: (Future enhancement)
- **Crypto**: Bitcoin, Ethereum, major altcoins via Coinbase/Kraken API
- **Internal Products**: Investing in scaling successful Builder Department products

**Think of it as:** A hedge fund trading desk with diverse strategies, rigorous risk management, and continuous learning from outcomes.

---

## ⚠️ Risk Management Philosophy

**CRITICAL**: This department trades real money. Safety mechanisms are non-negotiable.

### Core Risk Principles
1. **Position Limits**: No single trade > 5% of portfolio
2. **Diversification**: Max 20% in any single asset
3. **Stop Losses**: Every position has automatic stop loss
4. **Circuit Breakers**: Halt trading if daily loss > 10%
5. **Paper Trading Period**: All new strategies tested for 30 days before live capital
6. **Audit Trail**: Every trade logged with reasoning and outcome

### Two Operating Modes
```yaml
modes:
  paper_trading:
    enabled: true   # Safe default
    description: "Simulated trading with real market data, no real money"
    use_case: "Testing strategies, training new agents"

  live_trading:
    enabled: false  # Requires explicit activation
    description: "Real trades with real capital"
    requires: ["user_approval", "risk_management_validation", "30_day_paper_trading_success"]
```

**User must explicitly enable live trading and acknowledge risks.**

---

## 💼 Stockbroker Agent Types (6 Strategies)

Each stockbroker agent has a **primary trading strategy** influenced by their **personality traits**.

### 1. **Trend Follower**
**Strategy**: Identify and ride momentum trends (both up and down)
**Typical Holding Period**: 2-8 weeks
**Indicators Used**: Moving averages (50/200 SMA), MACD, volume analysis

**Personality Influence**:
- High risk_tolerance (0.70+): Larger positions, earlier entries (higher returns but more volatility)
- High analytical (0.85+): Waits for more confirmation signals (fewer trades, higher accuracy)
- High assertiveness (0.75+): Sticks with trades longer despite volatility
- Low risk_tolerance (0.35-): Smaller positions, more stop losses (lower returns, less drawdown)

**Example Identity**:
```yaml
name: "Yuki Tanaka"
age: 34
role: "Trend Follower"
personality:
  risk_tolerance: 0.72
  analytical: 0.88
  assertiveness: 0.79
  patience: 0.81
trading_philosophy: "The trend is your friend until it ends"
specialization: "Tech stocks, momentum plays"
typical_win_rate: 0.58
avg_return_per_trade: 0.08  # 8%
```

---

### 2. **Mean Reversion Trader**
**Strategy**: Buy oversold assets, sell overbought assets (contrarian)
**Typical Holding Period**: 3-14 days
**Indicators Used**: RSI, Bollinger Bands, support/resistance levels

**Personality Influence**:
- High openness (0.80+): More willing to buy when others panic
- Low optimism (0.35-): Better at identifying actual bottoms (not catching falling knives)
- High analytical (0.85+): Waits for statistical oversold conditions
- High risk_tolerance (0.70+): Buys during fear, sells during greed

**Example Identity**:
```yaml
name: "Dmitri Volkov"
age: 41
role: "Mean Reversion Trader"
personality:
  risk_tolerance: 0.68
  analytical: 0.92
  optimism: 0.32
  openness: 0.84
trading_philosophy: "Be greedy when others are fearful"
specialization: "Market crashes, oversold bounces"
typical_win_rate: 0.64
avg_return_per_trade: 0.06  # 6%
```

---

### 3. **Value Investor**
**Strategy**: Buy fundamentally strong companies at discount prices
**Typical Holding Period**: 3-12 months
**Analysis Used**: P/E ratios, revenue growth, competitive moats, earnings reports

**Personality Influence**:
- High patience (0.85+): Willing to hold through volatility
- High analytical (0.90+): Deep fundamental research
- Low risk_tolerance (0.30-): Only buys with margin of safety
- Low openness (0.40-): Sticks to proven value metrics, avoids hype

**Example Identity**:
```yaml
name: "Eleanor Park"
age: 47
role: "Value Investor"
personality:
  risk_tolerance: 0.28
  analytical: 0.94
  patience: 0.91
  openness: 0.38
trading_philosophy: "Price is what you pay, value is what you get"
specialization: "Undervalued blue chips, dividend aristocrats"
typical_win_rate: 0.71
avg_return_per_trade: 0.15  # 15% (but takes longer)
```

---

### 4. **Growth Hunter**
**Strategy**: Identify high-growth companies early, ride exponential growth
**Typical Holding Period**: 6-24 months
**Analysis Used**: Revenue growth rate, TAM (Total Addressable Market), competitive positioning

**Personality Influence**:
- High risk_tolerance (0.80+): Comfortable with volatility in growth stocks
- High optimism (0.75+): Believes in future potential despite high valuations
- High openness (0.85+): Early adopter of new technologies/sectors
- Low patience (0.40-): May exit winners too early

**Example Identity**:
```yaml
name: "Marcus Rodriguez"
age: 29
role: "Growth Hunter"
personality:
  risk_tolerance: 0.83
  optimism: 0.78
  openness: 0.89
  patience: 0.42
trading_philosophy: "Disruption creates fortunes"
specialization: "AI stocks, biotech, EVs, emerging tech"
typical_win_rate: 0.52
avg_return_per_trade: 0.22  # 22% (high variance)
```

---

### 5. **News/Event Trader**
**Strategy**: Trade based on news catalysts, earnings reports, product launches
**Typical Holding Period**: 1 hour - 3 days (very short-term)
**Data Sources**: Real-time news feeds, Twitter, Reddit, earnings calendars

**Personality Influence**:
- Low patience (0.25-): Quick in and out, doesn't hold overnight
- High analytical (0.85+): Quickly assesses news impact
- High assertiveness (0.80+): Acts fast on breaking news
- High risk_tolerance (0.75+): Comfortable with binary outcomes (earnings beats/misses)

**Example Identity**:
```yaml
name: "Aisha Chen"
age: 31
role: "News/Event Trader"
personality:
  risk_tolerance: 0.77
  analytical: 0.87
  patience: 0.21
  assertiveness: 0.84
trading_philosophy: "First to know, first to profit"
specialization: "Earnings plays, FDA approvals, product launches"
typical_win_rate: 0.61
avg_return_per_trade: 0.04  # 4% (but trades frequently)
```

---

### 6. **Portfolio Manager / Risk Coordinator**
**Strategy**: Doesn't trade directly - manages overall portfolio risk and allocation
**Responsibilities**:
- Monitors total portfolio exposure
- Enforces position limits
- Triggers circuit breakers
- Reallocates capital based on strategy performance
- Reports to Meta-Orchestrator

**Personality Influence**:
- Low risk_tolerance (0.20-): Conservative portfolio construction
- High analytical (0.95+): Quantitative risk modeling
- High assertiveness (0.85+): Will halt trading despite trader protests
- High empathy (0.70+): Balances trader autonomy with risk management

**Example Identity**:
```yaml
name: "Sarah Thompson"
age: 44
role: "Portfolio Manager"
personality:
  risk_tolerance: 0.18
  analytical: 0.96
  assertiveness: 0.87
  empathy: 0.73
management_philosophy: "Survive first, thrive second"
specialization: "Risk modeling, portfolio theory, crisis management"
```

---

## 📊 Trading Workflow

### Morning Routine (Market Open - 9:30 AM EST)

**1. Market Analysis** (All Traders, 9:00-9:30 AM)
```python
morning_analysis = {
    "macro_check": {
        "sp500_futures": "+0.8%",
        "vix": 18.2,  # Volatility index
        "news_sentiment": 0.62  # Positive
    },
    "sector_rotation": {
        "strongest": "Technology",
        "weakest": "Energy"
    },
    "scheduled_events": [
        "Fed Chair speech at 2 PM",
        "Tesla earnings after close"
    ]
}
```

**2. Trading Opportunities Identified** (9:30-10:00 AM)

**Trend Follower (Yuki)**:
- NVDA broke above 50-day SMA on high volume
- **Action**: Buy $2,000 position (4% of $50k portfolio)
- **Stop Loss**: 5% below entry
- **Target**: +12% (based on historical pattern)

**Mean Reversion (Dmitri)**:
- TSLA down 8% on no news, RSI at 28 (oversold)
- **Action**: Buy $1,500 position (3% of portfolio)
- **Stop Loss**: -6% from entry
- **Target**: +8% return to mean

**Value Investor (Eleanor)**:
- No trades today (waiting for quarterly earnings season)
- Monitoring existing positions
- Researching JNJ (P/E of 15, dividend yield 3.1%)

**Growth Hunter (Marcus)**:
- AI startup announced breakthrough model
- **Action**: Buy $2,500 in AI-related stocks (5% of portfolio)
- **Stop Loss**: -10% (accepts higher volatility)
- **Target**: +25%

**News Trader (Aisha)**:
- FDA approval expected for biotech stock (ticker: ABCD)
- **Action**: Wait for news, then trade within 5 minutes
- **Planned**: $1,000 position if approved

**Portfolio Manager (Sarah)**:
- **Current allocation**:
  - Cash: 30% ($15k)
  - Active positions: 70% ($35k)
  - Tech exposure: 25% (within 20% limit? NO - triggers warning)
- **Action**: "Team, we're overweight tech. No new tech positions until we sell something."

---

### Trade Execution Flow

```python
# Trader submits trade proposal
trade_proposal = {
    "trader": "yuki_tanaka",
    "strategy": "trend_following",
    "ticker": "NVDA",
    "action": "BUY",
    "amount_usd": 2000,
    "entry_price": 875.00,
    "stop_loss": 831.25,  # -5%
    "take_profit": 980.00,  # +12%
    "reasoning": "Broke above 50-day SMA with 2x average volume"
}

# Risk Management Validation (Automatic)
risk_check = validate_trade(trade_proposal)
"""
✅ Position size: 4.0% (under 5% limit)
✅ Portfolio allocation: Tech 22% (under 25% after adding this)
✅ Daily loss limit: -2.3% (under 10% circuit breaker)
✅ Stop loss set: Yes
✅ Available capital: $15,000 (sufficient)
"""

# Portfolio Manager Override Check
if risk_check.all_pass():
    if sarah_thompson.requires_approval(trade_proposal):
        # Personality check
        if trade_proposal.risk_score > sarah_thompson.risk_tolerance * 10:
            return "DENIED: Risk too high for current market conditions"

    # Execute trade via Alpaca API
    order = alpaca.submit_order(
        symbol="NVDA",
        qty=2.28,  # $2000 / $875
        side="buy",
        type="limit",
        limit_price=875.00,
        stop_loss={"stop_price": 831.25}
    )

    # Log to database
    log_trade(trade_proposal, order.id, "EXECUTED")
```

---

### Position Monitoring (Throughout Day)

**Real-Time Monitoring**:
- Every trader monitors their open positions
- Automatic alerts for stop loss triggers
- Personality influences exit decisions

**Example Scenario** (2:30 PM):
- Yuki's NVDA position: Entry $875, Current $892 (+2%)
- News: Fed Chair hints at rate hikes
- Market dips, NVDA drops to $880 (+0.6%)

**Yuki's Decision** (assertiveness: 0.79, patience: 0.81):
- Holds position (assertive enough to ride volatility)
- Doesn't panic sell (patient personality)
- Stop loss not triggered ($831)
- **Decision**: HOLD

**Alternate Personality** (assertiveness: 0.35, patience: 0.40):
- Gets nervous with volatility
- Exits at $880 for small gain (+0.6%)
- **Decision**: SELL (locks in small profit)

---

### End of Day Review (4:00-5:00 PM EST)

**Daily P&L** (Profit & Loss):
```python
daily_results = {
    "starting_portfolio": 50000,
    "ending_portfolio": 50425,
    "daily_return": 0.0085,  # +0.85%
    "trades_executed": 5,
    "trades_closed": 3,
    "by_trader": {
        "yuki_tanaka": +320,      # Trend trade working
        "dmitri_volkov": +180,    # Mean reversion winner
        "marcus_rodriguez": -150, # Growth trade stopped out
        "aisha_chen": +75         # News trade, quick profit
    }
}
```

**Recursive Learning Update**:
```python
# Track each trade outcome
for trade in closed_trades:
    update_trader_performance(
        trader=trade.trader,
        outcome=trade.pnl,
        strategy=trade.strategy,
        market_conditions=market_state
    )

    # Learn patterns
    if trade.pnl > 0:
        learn_pattern({
            "strategy": trade.strategy,
            "setup": trade.entry_reasoning,
            "market_regime": market_state.regime,
            "success": True
        })
```

---

## 🔄 Recursive Learning System

### 1. **Trader Performance Tracking**

**Every trade creates feedback data**:
```python
trade_outcome = {
    "trader_id": "yuki_tanaka",
    "trade_id": "uuid",
    "strategy": "trend_following",
    "entry_date": "2025-11-13",
    "exit_date": "2025-11-27",
    "holding_period_days": 14,
    "entry_price": 875.00,
    "exit_price": 980.00,
    "return_pct": 0.12,  # +12%
    "position_size_pct": 0.04,
    "market_conditions": {
        "regime": "bull_market",
        "vix": 16.2,
        "sp500_trend": "uptrend"
    },
    "outcome": "win"
}
```

**System learns**:
- Yuki's trend following works well in bull markets (78% win rate)
- Mean reversion (Dmitri) works better in choppy markets (71% win rate)
- Growth hunting (Marcus) underperforms in high-VIX environments

**Meta-Orchestrator adjusts**:
```python
# Bull market detected
if market_regime == "bull":
    allocate_more_capital_to("yuki_tanaka", multiplier=1.3)
    allocate_less_capital_to("dmitri_volkov", multiplier=0.7)

# High volatility detected
if vix > 25:
    reduce_position_sizes(multiplier=0.5)
    increase_cash_allocation(target=0.50)
```

---

### 2. **Strategy Evolution**

**Agents learn from each other's successes**:
```python
# Marcus (Growth) notices Aisha (News) is crushing it on FDA trades
pattern_observed = {
    "source_trader": "aisha_chen",
    "strategy": "fda_approval_plays",
    "win_rate": 0.73,
    "avg_return": 0.08,
    "market_conditions": "biotech_sector"
}

# Marcus's personality: openness=0.89 (high) → willing to learn
if marcus.openness > 0.75:
    marcus.adopt_strategy(pattern_observed)
    # Marcus now watches FDA calendar too

# Eleanor's personality: openness=0.38 (low) → skeptical
if eleanor.openness < 0.50:
    eleanor.ignore_strategy(pattern_observed)
    # Eleanor sticks to value investing
```

---

### 3. **Cross-Department Learning**

**Builder Department → Stockbrokers**:
```python
# Builder launches successful AI recipe optimizer
builder_outcome = {
    "product": "recipe-optimizer",
    "launch_date": "2025-11-20",
    "week_4_metrics": {
        "users": 1203,
        "dau": 412,
        "revenue": 1247.50
    },
    "outcome": "success"
}

# Growth Hunter (Marcus) analyzes
if marcus.sees_builder_success(builder_outcome):
    # Identifies similar public companies
    comparable_companies = ["ABNB", "DASH", "UBER"]  # Food/consumer tech

    # Increases position in similar stocks
    for ticker in comparable_companies:
        if market_data[ticker].momentum == "positive":
            marcus.increase_allocation(ticker, multiplier=1.2)

    # Alternatively: Suggests investing in scaling the product
    investment_proposal = {
        "target": "recipe-optimizer",
        "amount": 5000,
        "use": "Marketing budget to scale from 1.2k to 10k users",
        "expected_return": "3x in 6 months"
    }
```

**Idea Factory → Stockbrokers**:
```python
# Huginn discovers trending AI model on Twitter
scout_finding = {
    "source": "twitter",
    "trend": "New AI model 'Orion' by OpenAI competitor",
    "viral_velocity": 0.89,
    "sentiment": 0.92
}

# News Trader (Aisha) sees this IMMEDIATELY
if aisha.monitors_source("twitter") and scout_finding.viral_velocity > 0.80:
    # Identifies publicly traded beneficiaries
    related_stocks = ["NVDA", "AMD", "MSFT"]

    # Trades within 1 hour of scout finding
    for ticker in related_stocks:
        aisha.execute_trade(ticker, size=1000, hold_time="24_hours")
```

---

### 4. **Failure Learning (Hydra Protocol)**

**Scenario**: Dmitri (Mean Reversion) buys TSLA at $220 (down 8%, RSI 28)
- Reasoning: "Oversold, should bounce"
- Outcome: TSLA drops to $195 (-11% from entry), stop loss triggered
- **Loss**: -$165

**Failure Analysis**:
```python
failure_analysis = {
    "trader": "dmitri_volkov",
    "trade_id": "uuid",
    "loss_amount": -165,
    "loss_pct": -0.11,
    "strategy": "mean_reversion",
    "failure_reason_hypothesis": [
        "Caught falling knife - ignored broader bearish trend",
        "Company-specific negative news (recalled products)",
        "Mean reversion doesn't work in strong downtrends"
    ]
}

# System investigates
investigation = {
    "broader_market": "S&P 500 was down -2.1% that day (risk-off)",
    "sector": "Auto sector down -3.8% (sector weakness)",
    "company_news": "Product recall announced same morning (fundamental change)",
    "technical": "TSLA below 200-day SMA (long-term downtrend)"
}

# Pattern learned
new_pattern = {
    "pattern": "Don't buy mean reversion on bad news days",
    "confidence": 0.65,
    "sample_size": 1,  # Will gain confidence with more data
    "rule": "if RSI < 30 AND company_news_sentiment < 0.30 AND sector < -2%, SKIP trade"
}

# Dmitri's strategy updated
dmitri.add_filter(new_pattern)
```

**Hydra Effect** (New Capability):
```python
# System creates new validation agent
news_validator_agent = {
    "name": "News Impact Analyzer",
    "role": "Pre-trade validation",
    "task": "Check for material company news before mean reversion trades",
    "triggered_by_failure": "dmistri-tsla-001",
    "integration": "All mean reversion trades now require news clearance"
}

# Next time Dmitri wants to buy oversold:
trade_proposal = {...}
news_check = news_validator_agent.analyze(trade_proposal.ticker)
if news_check.negative_news_detected:
    return "DENIED: Material negative news detected"
```

**Result**: Failure created a smarter system.

---

## 🎛️ Granular Control Parameters

### Portfolio-Level Controls
```yaml
stockbrokers_department:
  trading_mode: paper  # paper | live

  portfolio:
    starting_capital: 50000.00
    max_total_exposure: 0.80  # Max 80% invested, 20% cash
    max_position_size: 0.05  # No position > 5%
    max_sector_concentration: 0.25  # No sector > 25%
    max_correlation: 0.70  # Avoid highly correlated positions
```

### Risk Management
```yaml
stockbrokers_department:
  risk_management:
    daily_loss_limit: 0.10  # Halt trading if down 10% in a day
    weekly_loss_limit: 0.15
    monthly_loss_limit: 0.20

    max_drawdown: 0.25  # Reduce size if down 25% from peak

    position_limits:
      require_stop_loss: true
      max_holding_period_days: 90  # Force review

    circuit_breakers:
      vix_threshold: 30  # Reduce size if VIX > 30
      market_crash: -0.05  # If S&P drops 5%, halt new trades
```

### Strategy Allocation
```yaml
stockbrokers_department:
  strategies:
    trend_following:
      enabled: true
      capital_allocation: 0.25  # 25% of active capital
      min_traders: 1
      max_traders: 3

    mean_reversion:
      enabled: true
      capital_allocation: 0.20

    value_investing:
      enabled: true
      capital_allocation: 0.20

    growth_hunting:
      enabled: true
      capital_allocation: 0.20

    news_trading:
      enabled: true
      capital_allocation: 0.15
```

### Personality Influence Tuning
```yaml
stockbrokers_department:
  personality_influence:
    enabled: true
    influence_strength: 0.80  # 0.0 = ignore personalities, 1.0 = full influence

    risk_tolerance_impact:
      on_position_size: 0.50  # High risk_tolerance → up to 50% larger positions
      on_stop_loss: 0.30  # High risk_tolerance → wider stop losses

    assertiveness_impact:
      on_exit_discipline: 0.60  # High assertiveness → sticks to plan

    patience_impact:
      on_holding_period: 0.70  # High patience → longer holds
```

### Learning System Controls
```yaml
stockbrokers_department:
  learning:
    enabled: true

    strategy_adaptation:
      min_sample_size: 20  # Need 20 trades before adjusting strategy
      confidence_threshold: 0.70  # 70% confidence to adopt new pattern

    capital_reallocation:
      enabled: true
      rebalance_frequency_days: 30
      performance_lookback_days: 90

      # Reallocate capital to best performers
      top_performer_bonus: 1.3  # Top trader gets 30% more capital
      bottom_performer_penalty: 0.7  # Bottom trader gets 30% less capital
```

---

## 📈 Success Metrics

### Portfolio Performance (Target Benchmarks)
```yaml
targets:
  annual_return: 0.15  # 15% annually (vs S&P 500 ~10%)
  sharpe_ratio: 1.5  # Risk-adjusted returns
  max_drawdown: -0.20  # No worse than -20% drawdown
  win_rate: 0.60  # 60% of trades profitable

  # Risk-adjusted
  calmar_ratio: 2.0  # Return / max drawdown
  sortino_ratio: 2.0  # Downside deviation focus
```

### Trader-Level Metrics
```yaml
trader_performance:
  - name: "Yuki Tanaka (Trend Follower)"
    trades_ytd: 45
    win_rate: 0.58
    avg_return_per_trade: 0.08
    total_return_ytd: 0.23  # 23%
    sharpe_ratio: 1.7
    max_drawdown: -0.12

  - name: "Eleanor Park (Value Investor)"
    trades_ytd: 12  # Fewer trades, longer holds
    win_rate: 0.71
    avg_return_per_trade: 0.15
    total_return_ytd: 0.19  # 19%
    sharpe_ratio: 2.1  # Lower volatility
    max_drawdown: -0.08
```

### Meta-Orchestrator Insights
```
STOCKBROKERS DEPARTMENT OVERVIEW (Last 90 Days)

Portfolio Value: $57,830 (Starting: $50,000)
Total Return: +15.7%
S&P 500 Return: +8.2% (outperformance: +7.5%)
Sharpe Ratio: 1.62
Max Drawdown: -8.3%

Best Performing Strategy: Trend Following (+28.4%)
Worst Performing Strategy: Growth Hunting (-4.2%)

Top Performer: Yuki Tanaka (Trend) - +$3,920
Learning Insight: Yuki's success rate increased from 58% → 67% after adopting
                  news validation filter from Aisha

Capital Reallocation Recommendation:
  ✅ Increase Trend Following allocation: 25% → 30%
  ⚠️ Reduce Growth Hunting allocation: 20% → 15% (underperforming in current high-rate environment)

Risk Management Status:
  ✅ All position limits respected
  ✅ No circuit breakers triggered
  ✅ Stop losses in place for all positions

Cross-Department Integration:
  💡 Idea Factory scout findings → Aisha traded 8 times, 6 winners (+$890)
  🏗️ Builder product success → Marcus increased ABNB position (+$340)

Pattern Learned:
  "Fed announcement days have 23% higher volatility. Reduce position sizes by 30%
   on scheduled Fed days." (Confidence: 0.81, Sample: 8 Fed days)
```

---

## 🔗 Integration with Other Departments

### Idea Factory → Stockbrokers
```python
# Scout discovers viral tweet about new AI breakthrough
scout_finding = {
    "source": "twitter",
    "content": "New AI model beats GPT-4 on benchmarks",
    "viral_velocity": 0.91,
    "timestamp": "2025-11-13T09:15:00Z"
}

# Aisha (News Trader) sees this in real-time
aisha.react_to_scout_finding(scout_finding)
# Buys NVDA, MSFT within 10 minutes
# Profit: +$420 (news trades)

# Outcome feeds back to scout
update_source_credibility("twitter", adjustment=+0.03)
update_agent_reputation("community_listener_3", adjustment=+0.05)
```

### Builder Department → Stockbrokers
```python
# Builder launches recipe optimizer, becomes successful
builder_success = {
    "product": "recipe-optimizer",
    "week_8_revenue": 4830,
    "growth_rate": 0.42  # 42% week-over-week
}

# Portfolio Manager proposes investment
investment_proposal = {
    "target": "recipe-optimizer",
    "amount": 10000,  # $10k from trading profits
    "use_case": "Hire contractor to build mobile app",
    "expected_outcome": "3x user growth, 4x revenue",
    "expected_return": "5x in 12 months"
}

# Meta-Orchestrator evaluates
if expected_return > stock_market_benchmark * 2:
    approve_investment(investment_proposal)

# Money flows from Stockbrokers → Builders
# Builders scale the product
# Increased revenue flows back to Stockbrokers
# Positive feedback loop
```

### Stockbrokers → Idea Factory
```python
# Stockbrokers notice pattern: AI infrastructure stocks outperforming
pattern_detected = {
    "sector": "AI Infrastructure",
    "stocks": ["NVDA", "AMD", "SMCI"],
    "performance_90d": [+45%, +38%, +52%],
    "insight": "Demand for AI compute is exploding"
}

# Sends signal to Idea Factory
signal_to_idea_factory = {
    "message": "AI infrastructure is hot. Scout for products that need GPU compute.",
    "actionable": True
}

# Huginn/Muninn adjust scout priorities
idea_factory.increase_scout_priority("AI infrastructure tools")

# Scouts find: "Developers complaining about GPU access costs on Reddit"
# Evaluation Committee approves: "GPU sharing marketplace" idea
# Builders create the product
# Product succeeds because Stockbrokers identified the trend early
```

---

## 🚨 Safety Mechanisms

### 1. **Circuit Breakers** (Automatic Trading Halts)
```python
circuit_breakers = {
    "daily_loss_10pct": {
        "trigger": "Portfolio down 10% in single day",
        "action": "HALT all new trades, emergency team meeting",
        "override": "Requires Portfolio Manager + Meta-Orchestrator approval"
    },
    "flash_crash": {
        "trigger": "S&P 500 down 5% in under 1 hour",
        "action": "HALT, close risky positions, go to cash",
        "override": "Requires manual user approval"
    },
    "position_limit_breach": {
        "trigger": "Single position > 5% due to price movement",
        "action": "Automatically trim position back to 5%",
        "override": "None (automatic risk management)"
    }
}
```

### 2. **Paper Trading Requirement**
```python
# All new strategies must pass 30-day paper trading
new_strategy = {
    "name": "Crypto Arbitrage",
    "trader": "new_agent_john",
    "status": "paper_trading",
    "start_date": "2025-11-01",
    "required_success": {
        "min_return": 0.05,  # 5% in 30 days
        "max_drawdown": -0.10,  # No worse than -10%
        "win_rate": 0.55
    }
}

# After 30 days
if new_strategy.paper_performance.meets_requirements():
    new_strategy.status = "approved_for_live"
    new_strategy.initial_capital = 1000  # Start with $1k
else:
    new_strategy.status = "rejected"
    # Agent must improve strategy or try different approach
```

### 3. **Audit Trail**
```sql
-- Every trade logged with full context
CREATE TABLE trade_log (
    trade_id UUID PRIMARY KEY,
    trader_id UUID NOT NULL,
    strategy VARCHAR(50) NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL,  -- BUY/SELL
    quantity DECIMAL(10, 4) NOT NULL,
    entry_price DECIMAL(10, 2) NOT NULL,
    entry_timestamp TIMESTAMP NOT NULL,
    exit_price DECIMAL(10, 2),
    exit_timestamp TIMESTAMP,
    pnl DECIMAL(10, 2),
    pnl_pct DECIMAL(6, 4),

    -- Reasoning and context
    entry_reasoning TEXT NOT NULL,
    market_conditions JSONB NOT NULL,
    risk_check_passed BOOLEAN NOT NULL,
    approved_by UUID,  -- Portfolio Manager

    -- Personality influence tracking
    trader_personality JSONB NOT NULL,
    personality_influenced_decision BOOLEAN,

    -- Outcome tracking
    outcome VARCHAR(20),  -- win/loss/breakeven
    lessons_learned TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);
```

### 4. **Mandatory Stop Losses**
```python
# EVERY position must have stop loss
def execute_trade(trade_proposal):
    if not trade_proposal.stop_loss:
        return TradeRejection(reason="Stop loss required for all trades")

    if trade_proposal.stop_loss_pct > 0.15:
        return TradeRejection(reason="Stop loss too wide (max 15%)")

    # Execute trade with guaranteed stop loss
    order = alpaca.submit_order(
        symbol=trade_proposal.ticker,
        qty=trade_proposal.quantity,
        side=trade_proposal.action,
        type="limit",
        limit_price=trade_proposal.entry_price,
        stop_loss={
            "stop_price": trade_proposal.stop_loss_price,
            "limit_price": trade_proposal.stop_loss_price * 0.98  # 2% slippage buffer
        }
    )
```

---

## 🎯 Real-World Implementation Notes

### Alpaca API Integration (Stock Trading)
```python
import alpaca_trade_api as tradeapi

class AlpacaTrader:
    def __init__(self, mode="paper"):
        if mode == "paper":
            self.api = tradeapi.REST(
                key_id=settings.alpaca_paper_key,
                secret_key=settings.alpaca_paper_secret,
                base_url="https://paper-api.alpaca.markets"  # Paper trading
            )
        else:
            self.api = tradeapi.REST(
                key_id=settings.alpaca_live_key,
                secret_key=settings.alpaca_live_secret,
                base_url="https://api.alpaca.markets"  # LIVE TRADING
            )

    def get_portfolio_value(self) -> float:
        account = self.api.get_account()
        return float(account.portfolio_value)

    def submit_trade(self, ticker, quantity, side, entry_price, stop_loss):
        order = self.api.submit_order(
            symbol=ticker,
            qty=quantity,
            side=side,  # buy or sell
            type="limit",
            time_in_force="day",
            limit_price=entry_price,
            stop_loss={"stop_price": stop_loss}
        )
        return order

    def get_positions(self):
        return self.api.list_positions()
```

### Real Market Data
```python
# Real-time stock prices (Alpaca provides free real-time data)
def get_current_price(ticker):
    latest_trade = api.get_latest_trade(ticker)
    return latest_trade.price

# Historical data for backtesting
def get_historical_data(ticker, start_date, end_date):
    bars = api.get_bars(
        ticker,
        timeframe="1Day",
        start=start_date,
        end=end_date
    ).df
    return bars

# Real-time news
def get_latest_news(ticker):
    news = api.get_news(ticker, limit=10)
    return news
```

### Crypto Trading Integration (Future Enhancement)
```python
# Coinbase API for crypto
import cbpro

class CoinbaseTrader:
    def __init__(self, mode="sandbox"):
        if mode == "sandbox":
            self.client = cbpro.AuthenticatedClient(
                key=settings.coinbase_sandbox_key,
                secret=settings.coinbase_sandbox_secret,
                passphrase=settings.coinbase_sandbox_passphrase,
                api_url="https://api-public.sandbox.pro.coinbase.com"
            )
        else:
            # LIVE CRYPTO TRADING
            self.client = cbpro.AuthenticatedClient(...)
```

---

## 🧪 Example Trading Day Walkthrough

**Date**: November 13, 2025
**Starting Portfolio**: $50,000
**Market**: S&P 500 +0.3%, Tech sector +0.8%

### 9:00 AM - Pre-Market Analysis

**Yuki (Trend Follower)** scans charts:
- NVDA: Broke above 50-day SMA yesterday, holding above
- Volume: 2.3x average (strong conviction)
- **Decision**: Add to watchlist, will buy if opens strong

**Dmitri (Mean Reversion)** scans for oversold:
- TSLA: Down 6% on no news, RSI 32
- Checks news validator: No material negative news ✅
- **Decision**: Will buy if opens weak (confirms oversold)

**Eleanor (Value)** reviews earnings calendar:
- JNJ reports tomorrow morning
- Current P/E: 15 (below 5-year avg of 17)
- **Decision**: Will buy after earnings if beat expected

**Marcus (Growth)** checks AI sector:
- New model announced by competitor to OpenAI
- Related stocks: NVDA, MSFT, GOOGL
- **Decision**: Will buy AI infrastructure stocks

**Aisha (News Trader)** monitors feeds:
- FDA decision expected today for biotech ABCD
- **Decision**: Wait for announcement, trade immediately after

### 9:30 AM - Market Open

**Yuki executes**:
- NVDA opens at $878 (up $3 from yesterday)
- Buys $2,000 position (2.28 shares)
- Stop loss at $834 (-5%)
- Target: $985 (+12%)

**Dmitri executes**:
- TSLA opens at $218 (down another 1%)
- Buys $1,500 position (6.88 shares)
- Stop loss at $205 (-6%)
- Target: $236 (+8%)

**Marcus executes**:
- Buys $1,000 NVDA, $1,000 MSFT
- Stop loss at -10% (accepts higher volatility)
- Target: +25%

**Sarah (Portfolio Manager)** reviews:
- Total exposure: 72% (within 80% limit) ✅
- Tech allocation: 24% (within 25% limit) ✅
- All stop losses in place ✅
- **Status**: All trades approved

### 11:30 AM - News Event

**FDA APPROVES DRUG FOR ABCD** 🚨

**Aisha (within 2 minutes)**:
- Sees news alert
- ABCD trading at $42 (was $38)
- Buys $1,000 position at $43.50 (already moving)
- Stop loss at $41 (-5.7%)
- Target: $48 (+10%)

**Personality influence**:
- Aisha (patience: 0.21, assertiveness: 0.84)
- Acts FAST (low patience = quick trigger)
- Doesn't hesitate (high assertiveness = confident execution)

**Alternate personality would**:
- Patience: 0.85, assertiveness: 0.40
- Waits for pullback (high patience)
- Hesitates, misses the move (low assertiveness)

### 2:00 PM - Position Management

**Current positions**:
- Yuki's NVDA: +2.5% (holding, target not hit)
- Dmitri's TSLA: -1.2% (holding, expecting bounce)
- Marcus's NVDA/MSFT: +1.8% / +0.9% (holding for bigger move)
- Aisha's ABCD: +6.2% (considering exit)

**Aisha's decision**:
- Target was +10%, currently +6.2%
- **Personality**: patience: 0.21 (very low)
- **Decision**: SELL (locks in +6.2%, $62 profit)
- Takes profit early due to low patience

**Alternate personality**:
- Patience: 0.80
- **Decision**: HOLD (waits for full +10% target)
- Risk: Might give back gains if reverses

### 4:00 PM - Market Close

**Final Positions**:
- Yuki's NVDA: +1.8% ($36 unrealized)
- Dmitri's TSLA: +3.2% ($48 unrealized)
- Marcus's NVDA/MSFT: +2.1% / +1.4% ($35 unrealized)
- Aisha's ABCD: CLOSED +6.2% ($62 realized) ✅

**Daily P&L**: +$181 (+0.36% on portfolio)

### 5:00 PM - End of Day Review

**Recursive Learning Updates**:
```python
# Aisha's FDA trade was successful
update_agent_reputation("aisha_chen", adjustment=+0.02)
update_strategy_confidence("fda_approval_plays", adjustment=+0.05)

# Dmitri's mean reversion working (TSLA bouncing)
update_strategy_confidence("mean_reversion_no_news", adjustment=+0.03)

# Pattern reinforced
reinforce_pattern({
    "pattern": "FDA approvals → immediate price jump → trade within 5 min",
    "confidence": 0.87,  # Was 0.82, now 0.87
    "sample_size": 9  # Was 8, now 9
})
```

**Meta-Orchestrator Notes**:
```
Daily Review - Nov 13, 2025

✅ Positive day: +0.36%
✅ All trades followed risk rules
✅ Aisha's news trading continues to perform (8/10 winners)

Recommendation:
  Consider increasing Aisha's capital allocation from $5k → $7k
  Her FDA strategy has 80% win rate over 10 trades

Learning:
  Dmitri's new news-validation filter prevented 2 bad trades this week
  Estimated losses avoided: $320
  Filter is working - keep enabled
```

---

**This is your Stockbrokers Department! Where market intelligence becomes real profits, and every trade makes the system smarter.** 📈

---

## ⚖️ Legal & Compliance Notes

**Disclaimer**: This system trades real money. Users must:
1. Understand trading risks (can lose entire capital)
2. Comply with local securities regulations
3. Use paper trading mode until strategies are validated
4. Never trade with money they can't afford to lose
5. Monitor the system actively (not fully autonomous initially)

**Recommended Approach**:
- Start with $1,000-$5,000 (small capital)
- Paper trade for 90 days minimum
- Gradually increase capital as confidence builds
- Always maintain emergency stop mechanisms
- Regular human oversight required

**This is not financial advice. Trade at your own risk.** ⚠️
