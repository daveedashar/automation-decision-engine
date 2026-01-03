# Automation Decision Engine

Rule-based and event-driven decision engine for business automation—handling complex logic, routing, and execution without manual intervention.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg)

---

## 🎯 Overview

This engine automates business decisions by evaluating rules, processing events, and executing actions—enabling consistent, repeatable execution at scale.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Event     │────▶│    Rule     │────▶│  Decision   │────▶│   Action    │
│   Input     │     │   Engine    │     │   Output    │     │   Executor  │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │   Audit     │
                    │    Log      │
                    └─────────────┘
```

---

## ✨ Features

- **Rule Engine** - Define complex business rules in YAML or code
- **Decision Trees** - Visual decision flow with branching logic
- **Event Processing** - React to real-time events from any source
- **Action Execution** - Trigger workflows, APIs, notifications
- **Audit Trail** - Complete logging of all decisions for compliance
- **A/B Testing** - Test different rule sets in production
- **Fallback Handling** - Graceful degradation when rules don't match

---

## 🏗️ Architecture

```
src/
├── api/                 # REST API
│   ├── decisions.py
│   ├── rules.py
│   └── events.py
├── core/                # Core engine
│   ├── rule_engine.py
│   ├── decision_tree.py
│   ├── evaluator.py
│   └── context.py
├── rules/               # Rule definitions
│   ├── parser.py
│   ├── validator.py
│   └── compiler.py
├── actions/             # Action executors
│   ├── base_action.py
│   ├── webhook_action.py
│   ├── email_action.py
│   └── workflow_action.py
├── storage/             # Persistence
│   ├── rule_store.py
│   └── decision_log.py
└── monitoring/          # Observability
    ├── metrics.py
    └── audit.py
```

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/daveedashar/automation-decision-engine.git
cd automation-decision-engine

# Install dependencies
pip install -r requirements.txt

# Run the service
python -m src.main
```

---

## 📋 Rule Definition (YAML)

```yaml
# rules/lead_routing.yaml
name: lead_routing
version: 1.0
description: Route leads based on score and region

rules:
  - name: high_value_enterprise
    conditions:
      all:
        - field: lead_score
          operator: gte
          value: 80
        - field: company_size
          operator: eq
          value: "enterprise"
    actions:
      - type: assign
        to: "enterprise_team"
      - type: notify
        channel: "slack"
        message: "🔥 High-value lead: {{lead.name}}"
    priority: 100

  - name: mid_market_qualified
    conditions:
      all:
        - field: lead_score
          operator: gte
          value: 50
        - field: company_size
          operator: in
          value: ["mid_market", "smb"]
    actions:
      - type: assign
        to: "sales_team"
      - type: add_to_sequence
        sequence: "nurture_qualified"
    priority: 50

  - name: default_routing
    conditions:
      all: []  # Catch-all
    actions:
      - type: assign
        to: "sdr_team"
    priority: 0
```

---

## 📋 Usage Example

### Evaluate a Decision

```python
from src.core import DecisionEngine

engine = DecisionEngine()
engine.load_rules("rules/lead_routing.yaml")

# Evaluate
result = engine.evaluate({
    "lead_score": 85,
    "company_size": "enterprise",
    "region": "north_america",
    "lead": {
        "name": "Acme Corp",
        "email": "john@acme.com"
    }
})

print(result)
# {
#     "rule_matched": "high_value_enterprise",
#     "actions": [
#         {"type": "assign", "to": "enterprise_team"},
#         {"type": "notify", "channel": "slack", ...}
#     ],
#     "decision_id": "dec_abc123",
#     "timestamp": "2026-01-03T22:30:00Z"
# }
```

### Define Rules in Code

```python
from src.core import Rule, Condition, Action

rule = Rule(
    name="fraud_detection",
    conditions=[
        Condition("transaction_amount", "gte", 10000),
        Condition("country", "in", ["high_risk_countries"]),
        Condition("velocity_24h", "gte", 5),
    ],
    match_type="all",  # or "any"
    actions=[
        Action("flag", severity="high"),
        Action("notify", team="fraud_ops"),
        Action("hold_transaction"),
    ]
)

engine.add_rule(rule)
```

---

## ⚙️ Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals | `field: status, operator: eq, value: "active"` |
| `neq` | Not equals | `field: type, operator: neq, value: "test"` |
| `gt` | Greater than | `field: amount, operator: gt, value: 100` |
| `gte` | Greater than or equal | `field: score, operator: gte, value: 50` |
| `lt` | Less than | `field: age, operator: lt, value: 30` |
| `lte` | Less than or equal | `field: count, operator: lte, value: 10` |
| `in` | In list | `field: country, operator: in, value: ["US", "UK"]` |
| `not_in` | Not in list | `field: status, operator: not_in, value: ["banned"]` |
| `contains` | Contains substring | `field: email, operator: contains, value: "@gmail"` |
| `regex` | Regex match | `field: phone, operator: regex, value: "^\+1"` |

---

## 📊 Decision Flow

```
EVENT RECEIVED
      │
      ▼
┌─────────────┐
│  Load Rules │
│  (Priority) │
└─────────────┘
      │
      ▼
┌─────────────┐     NO      ┌─────────────┐
│  Evaluate   │────────────▶│   Next      │
│  Conditions │             │   Rule      │
└─────────────┘             └─────────────┘
      │ YES                        │
      ▼                            │
┌─────────────┐                    │
│  Execute    │                    │
│  Actions    │                    │
└─────────────┘                    │
      │                            │
      ▼                            │
┌─────────────┐                    │
│  Log        │◀───────────────────┘
│  Decision   │     (if no match)
└─────────────┘
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# Test specific rules
python -m src.cli test-rule rules/lead_routing.yaml --input test_data.json
```

---

## 📈 Outcomes

- **Eliminated** manual decision bottlenecks
- **100% consistent** execution across all cases
- **< 50ms** decision latency
- **Complete audit trail** for compliance

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Daud Ashar**  
- GitHub: [@daveedashar](https://github.com/daveedashar)
- LinkedIn: [/in/daudashar](https://linkedin.com/in/daudashar)
- Email: daud-a@consultant.com
