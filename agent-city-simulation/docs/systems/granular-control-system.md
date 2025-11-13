# Granular Control System - Complete Parameter Management
*"Every knob, every dial, every threshold - all adjustable without code changes."*

## 🎛️ Philosophy

**Zero Code Changes for Tuning**

Every behavior in the system is controlled by configuration parameters that can be:
- ✅ Adjusted without code deployment
- ✅ Changed at runtime via API
- ✅ Overridden per-agent, per-department, or globally
- ✅ A/B tested between different values
- ✅ Rolled back instantly if something breaks
- ✅ Versioned and tracked over time
- ✅ Validated before application

---

## 📁 Configuration Hierarchy

```
Global Config (system-wide defaults)
    ↓
Department Config (overrides for department)
    ↓
Agent Type Config (overrides for agent class)
    ↓
Individual Agent Config (overrides for specific agent)
    ↓
Runtime Override (temporary, highest priority)
```

**Example:**
```yaml
# Global: All agents have confidence threshold 0.65
confidence_threshold: 0.65

# Department: R&D department uses 0.60
departments:
  rd:
    confidence_threshold: 0.60

# Agent Type: News Hunters use 0.70 (more aggressive)
agent_types:
  news_hunter:
    confidence_threshold: 0.70

# Individual: huginn_news_07 uses 0.75 (top performer, higher standards)
agents:
  huginn_news_07:
    confidence_threshold: 0.75

# Runtime: Emergency - lower to 0.50 for next hour
runtime_overrides:
  - parameter: confidence_threshold
    value: 0.50
    expires_at: 2025-11-14T15:00:00Z
```

**Resolution Order:**
```
Runtime Override (0.50)
  → Individual Agent (0.75)
    → Agent Type (0.70)
      → Department (0.60)
        → Global (0.65)

Result: 0.50 (runtime override wins)
```

---

## 🎚️ Complete Parameter Catalog

### **1. Learning System Parameters**

```yaml
learning_parameters:

  # Source Weight Adjustment
  source_learning:
    initial_weight: 1.0000  # Starting weight for new sources
    min_weight: 0.1000  # Floor (never go below)
    max_weight: 2.0000  # Ceiling (never go above)

    # Adjustment based on accuracy
    weight_adjustments:
      very_accurate:  # prediction error < 0.1
        amount: +0.0500
      accurate:  # error < 0.2
        amount: +0.0200
      neutral:  # error < 0.3
        amount: 0.0000
      inaccurate:  # error >= 0.3
        amount: -0.0300

    # Learning rate (how fast we adjust)
    learning_rate: 0.1000

    # Exponential moving average alpha
    ema_alpha: 0.1000

    # Minimum outcomes before adjusting weights
    min_outcomes_for_adjustment: 3

    # Temporal decay
    temporal_decay:
      enabled: true
      decay_start_days: 90  # Start decaying after 90 days inactive
      decay_rate: 0.9500  # 5% decay per month
      decay_interval_days: 30

  # Pattern Learning
  pattern_learning:
    initial_confidence: 0.5000  # Unknown patterns start neutral
    min_occurrences_to_learn: 3  # Need 3 occurrences to establish pattern
    similarity_threshold: 0.8500  # How similar patterns must be to match

    # Success rate calculation
    success_threshold: 0.6000  # outcome > 0.6 = success

    # Pattern aging
    pattern_decay:
      enabled: true
      decay_after_days: 180  # Patterns decay after 6 months
      decay_rate: 0.9800  # 2% decay per month

  # Agent Reputation
  agent_reputation:
    initial_reputation: 0.5000  # New agents start neutral
    learning_rate: 0.1000  # How fast reputation changes

    # Performance thresholds
    top_performer_threshold: 0.7500
    needs_retraining_threshold: 0.3500

    # Specialization detection
    specialization:
      min_category_ratio: 0.7000  # 70% of successes in one category
      min_successes_required: 5  # Need 5 successes to detect specialty

    # Reputation decay (prevent resting on laurels)
    reputation_decay:
      enabled: true
      decay_after_days: 60
      decay_rate: 0.9900  # 1% decay per month

# Attribution Weights
attribution:
  scout_agent_weight: 0.4000  # 40% credit to finder
  evaluator_weight: 0.3000  # 30% credit to evaluators
  builder_weight: 0.3000  # 30% credit to builders
```

---

### **2. Exploration/Exploitation Parameters**

```yaml
exploration_parameters:

  # Core Balance
  exploitation_ratio: 0.8000  # 80% exploitation
  exploration_ratio: 0.2000  # 20% exploration

  # Dynamic adjustment ranges
  adjustment:
    min_exploration: 0.1500  # Never go below 15%
    max_exploration: 0.4000  # Never go above 40%

    # Triggers for adjustment
    triggers:
      low_diversity:
        threshold: 0.5000
        increase_exploration_by: +0.1000

      high_success_rate:
        threshold: 0.8000
        increase_exploration_by: +0.0500

      market_volatility_high:
        threshold: 0.7000
        increase_exploration_by: +0.0800

      long_since_discovery:
        days: 30
        increase_exploration_by: +0.1200

  # Wild Card Cycles
  wild_card:
    enabled: true
    frequency: 5  # Every 5th cycle

    # Wild card behavior
    ignore_source_weights: true
    ignore_pattern_history: true
    lower_confidence_threshold_to: 0.4000
    contrarian_mode: true

    # Sampling strategy
    new_sources_pct: 0.5000  # 50% try never-used sources
    low_weight_sources_pct: 0.3000  # 30% revisit low-weight
    random_platforms_pct: 0.2000  # 20% try new platforms

  # Contrarian Quota
  contrarian:
    enabled: true
    minimum_ratio: 0.1000  # At least 10% contrarian
    target_ratio: 0.1500  # Target 15%

    # Contrarian agent count
    contrarian_agent_count: 3
    standard_agent_count: 15

  # Diversity Thresholds
  diversity:
    source_coverage_min: 0.4000  # Use at least 40% of sources
    unique_patterns_min: 5  # At least 5 different patterns
    single_source_max_pct: 0.4000  # No source >40% of findings
    topic_diversity_min: 0.3000  # No single topic >70%
```

---

### **3. Agent Behavior Parameters**

```yaml
agent_parameters:

  # Global Agent Settings
  global:
    scout_cycle_hours: 10
    max_concurrent_scouts: 300
    heartbeat_interval_seconds: 30
    timeout_seconds: 300
    retry_attempts: 3
    retry_backoff_factor: 2.0

  # Per-Agent-Type Settings
  agent_types:

    news_hunter:
      personality:
        speed: 0.9000  # Very fast (0-1)
        thoroughness: 0.6000  # Moderate depth
        risk_tolerance: 0.7000  # Fairly aggressive
        contrarian_tendency: 0.3000  # Somewhat conventional

      behavior:
        confidence_threshold: 0.7000
        max_findings_per_cycle: 15
        sources_to_check: 12
        rush_mode_enabled: true  # Can scout faster if urgent
        rush_threshold: 0.8500  # Urgency > 0.85 triggers rush

      scoring_weights:
        velocity: 0.3500  # How fast spreading
        credibility: 0.2500  # Source quality
        novelty: 0.2000  # How new
        relevance: 0.2000  # Market fit

    community_listener:
      personality:
        speed: 0.4000  # Slow and thorough
        thoroughness: 0.9500  # Very deep
        risk_tolerance: 0.5000  # Balanced
        contrarian_tendency: 0.4000  # Somewhat contrarian

      behavior:
        confidence_threshold: 0.6000
        max_findings_per_cycle: 8
        sources_to_check: 6
        deep_dive_mode: true
        comments_to_read: 100
        thread_depth: 3  # How deep to read comment chains

      scoring_weights:
        pain_intensity: 0.4000  # How much people care
        frequency: 0.2500  # How often mentioned
        willingness_to_pay: 0.2500  # Pay indicators
        workaround_presence: 0.1000  # Hacky solutions exist

    trend_analyst:
      personality:
        speed: 0.6000
        thoroughness: 0.7000
        risk_tolerance: 0.6000
        contrarian_tendency: 0.7000  # Often contrarian

      behavior:
        confidence_threshold: 0.6500
        max_findings_per_cycle: 10
        historical_lookback_days: 90
        prediction_horizon_days: 45

      scoring_weights:
        growth_velocity: 0.3500
        cross_platform_correlation: 0.3000
        longevity_score: 0.2000
        market_size: 0.1500

    technology_scout:
      personality:
        speed: 0.7000
        thoroughness: 0.8000
        risk_tolerance: 0.8000  # Very risk-tolerant
        contrarian_tendency: 0.6000

      behavior:
        confidence_threshold: 0.6000
        max_findings_per_cycle: 12
        tech_adoption_threshold: 0.0500  # 5% adoption = interesting

      scoring_weights:
        adoption_velocity: 0.3000
        developer_sentiment: 0.2500
        use_case_diversity: 0.2500
        integration_potential: 0.2000

    sentiment_monitor:
      personality:
        speed: 0.8000  # Fast, reactive
        thoroughness: 0.5000
        risk_tolerance: 0.5000
        contrarian_tendency: 0.2000  # Follows mood

      behavior:
        confidence_threshold: 0.6500
        max_findings_per_cycle: 10
        sentiment_shift_threshold: 0.2000  # 20% change = significant

      scoring_weights:
        sentiment_magnitude: 0.3500
        sentiment_velocity: 0.3000  # How fast changing
        volume: 0.2000
        authenticity: 0.1500  # Not astroturfed

    economic_watcher:
      personality:
        speed: 0.5000
        thoroughness: 0.9000
        risk_tolerance: 0.4000  # Conservative
        contrarian_tendency: 0.5000

      behavior:
        confidence_threshold: 0.7500  # High bar
        max_findings_per_cycle: 6
        economic_indicator_weight: 0.8000

      scoring_weights:
        capital_flow_magnitude: 0.4000
        market_timing: 0.3000
        risk_level: 0.2000
        opportunity_window: 0.1000
```

---

### **4. Audit & Monitoring Parameters**

```yaml
audit_parameters:

  # Diversity Auditor
  diversity_auditor:
    enabled: true
    frequency: "daily"  # daily, weekly, per_cycle

    thresholds:
      source_diversity_min: 0.5000
      pattern_diversity_min: 6
      contrarian_ratio_min: 0.1000
      topic_diversity_min: 0.3000
      overall_diversity_min: 0.6500

    actions:
      trigger_exploration_below: 0.6000
      alert_below: 0.5000
      emergency_exploration_below: 0.4000

  # Market Shift Detector
  market_shift_detection:
    enabled: true
    check_frequency: "weekly"

    # Pattern performance monitoring
    lookback_days: 30
    historical_comparison_days: 90

    # Shift thresholds
    decline_threshold: 0.3000  # -30% = shift detected
    confidence_threshold: 0.8000  # 80% confident

    # Actions on detection
    actions:
      mark_pattern_declining: true
      trigger_exploration: true
      alert_departments: true
      revalidation_required: true

  # Monthly Audit
  monthly_audit:
    enabled: true
    day_of_month: 1  # Run on 1st of month

    reports:
      - diversity_analysis
      - source_performance
      - agent_performance
      - pattern_evolution
      - exploration_roi
      - market_adaptations

    auto_actions:
      temporal_decay: true
      agent_retraining_recommendations: true
      source_pruning: false  # Manual only
```

---

### **5. Opportunity Scoring Parameters**

```yaml
scoring_parameters:

  # Opportunity Score Calculation
  opportunity_scoring:
    weights:
      market_potential: 0.2500
        sub_weights:
          market_size: 0.6000
          growth_rate: 0.4000

      feasibility: 0.2000
        sub_weights:
          technical_difficulty: 0.4000
          time_to_market: 0.3000
          resource_requirements: 0.3000

      timing: 0.2000
        sub_weights:
          urgency: 0.5000
          competition: 0.3000
          trend_lifecycle: 0.2000

      confidence: 0.2000
        sub_weights:
          data_quality: 0.4000
          source_credibility: 0.3000
          cross_validation: 0.3000

      strategic_fit: 0.1500
        sub_weights:
          alignment_with_goals: 0.6000
          synergies: 0.4000

  # Filtering Thresholds
  filters:
    minimum_thresholds:
      confidence: 0.6500
      market_size: 0.4000
      data_quality: 0.5000

    priority_flags:
      urgent:
        confidence_gt: 0.8000
        urgency_gt: 0.7500

      high_value:
        market_size_gt: 0.8000
        growth_rate_gt: 0.7000

      quick_win:
        time_to_market_lt: 0.3000
        feasibility_gt: 0.7000

      strategic:
        trend_lifecycle: "early"
        market_size_gt: 0.6000
```

---

### **6. Department-Specific Parameters**

```yaml
department_parameters:

  idea_factory:
    enabled: true
    agent_count: 18

    scout_cycle:
      duration_hours: 10
      concurrent_cycles: 1
      rush_mode_enabled: true

    output:
      min_findings_per_cycle: 3
      max_findings_per_cycle: 20
      auto_filter: true
      auto_rank: true

    data_retention:
      findings_days: 90
      raw_data_days: 30
      outcomes_days: 365

  rd_department:
    enabled: true
    agent_count: 10

    research_cycle:
      duration_hours: 24
      analysis_depth: "deep"  # shallow, medium, deep

    collaboration:
      share_with:
        - builders
        - stockbrokers
      report_frequency_hours: 24
      min_confidence_to_share: 0.6000

  builders:
    enabled: true
    agent_count: 10

    build_pipeline:
      idea_evaluation_threshold: 0.7000
      prototype_speed: "normal"  # fast, normal, thorough
      testing_rigor: "medium"  # low, medium, high

    timelines:
      idea_to_prototype_hours: 120  # 5 days
      prototype_to_launch_hours: 180  # 7.5 days

  stockbrokers:
    enabled: false  # Safe default
    agent_count: 10

    trading_mode: "paper"  # paper, live

    risk_management:
      max_capital_per_agent: 500.00
      max_position_size: 100.00
      max_positions_per_agent: 10
      daily_loss_limit: 50.00
      max_drawdown_pct: 0.1000

      diversification:
        min_assets: 5
        max_sector_exposure_pct: 0.3000

    strategy:
      approach: "diversified"  # conservative, balanced, diversified, aggressive
      time_horizon: "medium"  # short, medium, long

      confidence_threshold_to_trade: 0.7500
```

---

## 🔧 Runtime Control API

### **Get Current Configuration**

```bash
GET /api/config/{scope}

# Examples:
GET /api/config/global
GET /api/config/department/idea_factory
GET /api/config/agent_type/news_hunter
GET /api/config/agent/huginn_news_07
```

### **Update Configuration**

```bash
POST /api/config/{scope}
Content-Type: application/json

{
  "parameter": "learning_parameters.source_learning.initial_weight",
  "value": 1.1000,
  "reason": "Increasing initial trust in new sources",
  "expires_at": null  # Permanent, or timestamp for temporary
}
```

### **Create Runtime Override**

```bash
POST /api/config/override
Content-Type: application/json

{
  "scope": "global",  # or "department/idea_factory" or "agent/huginn_news_07"
  "parameter": "exploration_ratio",
  "value": 0.3000,
  "reason": "Emergency exploration mode - market shift detected",
  "expires_at": "2025-11-14T18:00:00Z",  # Auto-reverts after
  "priority": "high"
}
```

### **A/B Test Configuration**

```bash
POST /api/config/ab_test
Content-Type: application/json

{
  "name": "Higher Exploration Ratio Test",
  "parameter": "exploration_ratio",
  "variants": [
    {"name": "control", "value": 0.2000, "agent_pct": 0.5},
    {"name": "test", "value": 0.3000, "agent_pct": 0.5}
  ],
  "duration_days": 14,
  "success_metric": "discoveries_per_cycle"
}
```

### **Bulk Update**

```bash
POST /api/config/bulk_update
Content-Type: application/json

{
  "changes": [
    {
      "parameter": "agent_parameters.global.scout_cycle_hours",
      "value": 8
    },
    {
      "parameter": "exploration_parameters.exploration_ratio",
      "value": 0.2500
    },
    {
      "parameter": "department_parameters.idea_factory.agent_count",
      "value": 20
    }
  ],
  "reason": "Performance optimization based on monthly audit",
  "rollback_plan": "automatic_on_failure"
}
```

---

## 📊 Configuration Dashboard

```yaml
dashboard_features:

  # Real-time Parameter View
  parameter_explorer:
    - hierarchical_view  # See all levels of config
    - search_parameters
    - filter_by_department
    - show_effective_value  # After all overrides
    - show_override_chain  # Trace resolution

  # Quick Adjustments
  quick_controls:
    - exploration_ratio_slider  # 15-40%
    - confidence_threshold_slider  # 50-90%
    - agent_count_adjustment  # +/- agents
    - scout_cycle_frequency  # 4-12 hours
    - learning_rate_tuning  # 0.05-0.20

  # A/B Test Manager
  ab_test_dashboard:
    - active_tests_list
    - test_performance_metrics
    - early_stopping_if_clear_winner
    - auto_apply_winner_option

  # Safety Controls
  safety:
    - parameter_validation  # Prevent invalid values
    - change_confirmation  # Require approval for risky changes
    - rollback_button  # Instant revert
    - audit_trail  # Who changed what when

  # Presets
  preset_configs:
    - conservative_mode  # Low risk, high confidence thresholds
    - aggressive_mode  # High exploration, lower confidence
    - discovery_mode  # Maximum exploration temporarily
    - optimization_mode  # Maximize exploitation temporarily
    - balanced_mode  # Default recommended settings
```

---

## 🔒 Safety & Validation

### **Parameter Constraints**

```yaml
constraints:

  # Numeric ranges
  learning_parameters.source_learning.min_weight:
    type: float
    min: 0.0100
    max: 1.0000
    default: 0.1000

  learning_parameters.source_learning.max_weight:
    type: float
    min: 1.0000
    max: 5.0000
    default: 2.0000

  exploration_parameters.exploration_ratio:
    type: float
    min: 0.1000  # Never go below 10% exploration
    max: 0.5000  # Never go above 50%
    default: 0.2000
    warning_below: 0.1500
    warning_above: 0.4000

  # Logical constraints
  agent_count:
    type: integer
    min: 1
    max: 500
    recommended_max: 300

  # Dependent constraints
  validation_rules:
    - rule: "source_learning.min_weight < source_learning.max_weight"
      error_message: "Minimum weight must be less than maximum weight"

    - rule: "exploration_ratio + exploitation_ratio == 1.0"
      error_message: "Exploration + exploitation must equal 100%"

    - rule: "stockbrokers.trading_mode == 'live' requires approval"
      error_message: "Live trading requires explicit approval"
```

### **Change Approval Workflow**

```yaml
approval_required_for:
  - parameter: "stockbrokers.trading_mode"
    value: "live"
    approvers: ["admin", "finance_lead"]
    reason: "Real money at risk"

  - parameter: "exploration_ratio"
    value_gt: 0.35
    approvers: ["admin"]
    reason: "High exploration may reduce short-term performance"

  - parameter: "department_parameters.*.enabled"
    value: false
    approvers: ["admin"]
    reason: "Disabling entire department"
```

---

## 📜 Configuration Versioning

```yaml
versioning:

  # Auto-save snapshots
  auto_snapshot:
    frequency: "daily"
    retention_days: 90
    on_significant_change: true  # Save before big changes

  # Manual snapshots
  manual_snapshot:
    name: "Pre-launch configuration"
    timestamp: "2025-11-13T14:30:00Z"
    tags: ["stable", "tested", "production-ready"]

  # Rollback
  rollback_options:
    - to_snapshot: "snapshot_id"
    - to_timestamp: "2025-11-12T10:00:00Z"
    - to_tag: "stable"
    - to_previous: true  # Last known good

  # Change history
  audit_trail:
    - timestamp: "2025-11-13T14:30:00Z"
      user: "admin@agent-city.com"
      changes:
        - parameter: "exploration_ratio"
          old_value: 0.2000
          new_value: 0.2500
      reason: "Increasing exploration based on audit recommendations"
      snapshot_id: "snap_123"
```

---

## 🧪 Gradual Rollout

```yaml
rollout_strategy:

  # Canary deployment of config changes
  canary:
    enabled: true
    initial_pct: 0.1000  # Start with 10% of agents
    increment_pct: 0.2000  # Increase by 20% each step
    increment_interval_hours: 24

    success_criteria:
      - metric: "error_rate"
        threshold_lt: 0.0500  # <5% errors
      - metric: "performance_change"
        threshold_gt: -0.1000  # Not >10% worse

    auto_rollback:
      enabled: true
      on_failure: "immediate"
      on_degradation: "after_2_intervals"

  # Feature flags
  feature_flags:
    - name: "new_exploration_algorithm"
      enabled_for: ["huginn_news_07", "muninn_community_03"]  # Specific agents
      rollout_pct: 0.2000  # Or 20% random sample
      evaluate_after_days: 7
```

---

## 💾 Configuration Storage

```sql
-- Configuration storage schema

CREATE TABLE config.parameter_definitions (
    id UUID PRIMARY KEY,
    parameter_path VARCHAR(500) NOT NULL,  -- e.g., "learning_parameters.source_learning.initial_weight"
    value_type VARCHAR(50) NOT NULL,  -- float, int, bool, string, json
    default_value TEXT,
    min_value TEXT,
    max_value TEXT,
    description TEXT,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(parameter_path)
);

CREATE TABLE config.parameter_values (
    id UUID PRIMARY KEY,
    parameter_id UUID REFERENCES config.parameter_definitions(id),
    scope VARCHAR(100) NOT NULL,  -- global, department:name, agent_type:name, agent:id
    value TEXT NOT NULL,
    set_by VARCHAR(255),  -- User who set it
    reason TEXT,
    valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valid_until TIMESTAMP,  -- NULL = permanent
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE config.parameter_overrides (
    id UUID PRIMARY KEY,
    parameter_id UUID REFERENCES config.parameter_definitions(id),
    scope VARCHAR(100),
    override_value TEXT NOT NULL,
    priority INT DEFAULT 0,  -- Higher = takes precedence
    reason TEXT,
    set_by VARCHAR(255),
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE config.ab_tests (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    parameter_id UUID REFERENCES config.parameter_definitions(id),
    variants JSONB,  -- Array of {name, value, agent_pct}
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    success_metric VARCHAR(100),
    status VARCHAR(50),  -- active, completed, cancelled
    winner VARCHAR(100),  -- Variant name
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE config.configuration_snapshots (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    snapshot_data JSONB,  -- Complete config at this point
    tags TEXT[],
    created_by VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE config.change_audit_log (
    id BIGSERIAL PRIMARY KEY,
    parameter_path VARCHAR(500),
    scope VARCHAR(100),
    old_value TEXT,
    new_value TEXT,
    changed_by VARCHAR(255),
    reason TEXT,
    snapshot_id UUID REFERENCES config.configuration_snapshots(id),
    change_type VARCHAR(50),  -- set, override, ab_test, rollback
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_param_values_scope ON config.parameter_values(scope);
CREATE INDEX idx_param_overrides_active ON config.parameter_overrides(expires_at) WHERE expires_at > CURRENT_TIMESTAMP;
CREATE INDEX idx_audit_log_timestamp ON config.change_audit_log(created_at DESC);
```

---

## 🎯 Usage Examples

### **Example 1: Adjust Learning Rate**

```bash
# Via API
curl -X POST http://localhost:8000/api/config/global \
  -H "Content-Type: application/json" \
  -d '{
    "parameter": "learning_parameters.source_learning.learning_rate",
    "value": 0.15,
    "reason": "Speeding up adaptation to new sources"
  }'

# Via Dashboard
Navigate to: Config > Learning Parameters > Source Learning > Learning Rate
Slider: 0.10 → 0.15
Save with reason: "Speeding up adaptation"
```

### **Example 2: Emergency Exploration Mode**

```bash
# Market shift detected, need to explore more
curl -X POST http://localhost:8000/api/config/override \
  -d '{
    "scope": "global",
    "parameter": "exploration_ratio",
    "value": 0.35,
    "reason": "Market shift detected in privacy patterns",
    "expires_at": "2025-11-15T00:00:00Z",
    "priority": 100
  }'
```

### **Example 3: Per-Agent Tuning**

```python
# Top performer gets higher standards
await config_manager.set_parameter(
    scope="agent:huginn_news_07",
    parameter="confidence_threshold",
    value=0.80,
    reason="Top performer, can handle higher bar"
)

# Struggling agent gets more support
await config_manager.set_parameter(
    scope="agent:muninn_community_05",
    parameter="confidence_threshold",
    value=0.55,
    reason="Needs confidence boost during retraining"
)
```

### **Example 4: A/B Test New Algorithm**

```python
# Test higher exploration ratio
ab_test = await config_manager.create_ab_test(
    name="Exploration Ratio 25% vs 20%",
    parameter="exploration_ratio",
    variants=[
        {"name": "control", "value": 0.20, "agent_pct": 0.50},
        {"name": "test", "value": 0.25, "agent_pct": 0.50}
    ],
    duration_days=14,
    success_metric="valuable_discoveries_per_week"
)

# After 14 days, system auto-applies winner
```

---

## ✅ Result

**Every single behavior in the system is configurable without touching code:**

- ✅ Learning rates and thresholds
- ✅ Exploration/exploitation balance
- ✅ Agent personalities and behaviors
- ✅ Scoring weights
- ✅ Risk management parameters
- ✅ Audit frequencies
- ✅ Department settings
- ✅ Everything!

**Control mechanisms:**
- ✅ YAML configuration files
- ✅ Runtime API
- ✅ Web dashboard
- ✅ A/B testing
- ✅ Gradual rollouts
- ✅ Instant rollback
- ✅ Full audit trail

**Safety features:**
- ✅ Validation before changes
- ✅ Approval workflows for risky changes
- ✅ Configuration versioning
- ✅ Automatic snapshots
- ✅ Rollback on degradation

**You have complete granular control over the entire system!** 🎛️
