"""
Tests for rule engine.
"""

import pytest
from src.services.rule_engine import RuleEngine, Rule, Condition, Operator


@pytest.fixture
def rule_engine():
    return RuleEngine()


class TestRuleEngine:
    
    def test_evaluate_simple_condition(self, rule_engine):
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            conditions=[
                Condition(field="score", operator=Operator.GTE, value=80)
            ],
            match_type="all",
            actions=[{"type": "assign", "config": {"to": "team_a"}}],
        )
        rule_engine.add_rule(rule)
        
        # Should match
        result = rule_engine.evaluate({"score": 85})
        assert result is not None
        assert result.id == "test_rule"
        
        # Should not match
        result = rule_engine.evaluate({"score": 50})
        assert result is None
    
    def test_evaluate_all_conditions(self, rule_engine):
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            conditions=[
                Condition(field="score", operator=Operator.GTE, value=80),
                Condition(field="status", operator=Operator.EQ, value="active"),
            ],
            match_type="all",
            actions=[],
        )
        rule_engine.add_rule(rule)
        
        # Both conditions match
        result = rule_engine.evaluate({"score": 85, "status": "active"})
        assert result is not None
        
        # Only one condition matches
        result = rule_engine.evaluate({"score": 85, "status": "inactive"})
        assert result is None
    
    def test_evaluate_any_conditions(self, rule_engine):
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            conditions=[
                Condition(field="score", operator=Operator.GTE, value=80),
                Condition(field="priority", operator=Operator.EQ, value="high"),
            ],
            match_type="any",
            actions=[],
        )
        rule_engine.add_rule(rule)
        
        # One condition matches
        result = rule_engine.evaluate({"score": 50, "priority": "high"})
        assert result is not None
    
    def test_priority_ordering(self, rule_engine):
        low_priority = Rule(
            id="low",
            name="Low Priority",
            conditions=[Condition(field="score", operator=Operator.GTE, value=50)],
            match_type="all",
            actions=[],
            priority=10,
        )
        high_priority = Rule(
            id="high",
            name="High Priority",
            conditions=[Condition(field="score", operator=Operator.GTE, value=50)],
            match_type="all",
            actions=[],
            priority=100,
        )
        
        rule_engine.add_rule(low_priority)
        rule_engine.add_rule(high_priority)
        
        result = rule_engine.evaluate({"score": 75})
        assert result.id == "high"
    
    def test_nested_field_access(self, rule_engine):
        rule = Rule(
            id="test_rule",
            name="Test Rule",
            conditions=[
                Condition(field="user.profile.level", operator=Operator.EQ, value="premium")
            ],
            match_type="all",
            actions=[],
        )
        rule_engine.add_rule(rule)
        
        context = {
            "user": {
                "profile": {
                    "level": "premium"
                }
            }
        }
        
        result = rule_engine.evaluate(context)
        assert result is not None
