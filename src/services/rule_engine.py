"""
Rule engine for evaluating conditions and executing actions.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import re
import operator


class Operator(Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    REGEX = "regex"


@dataclass
class Condition:
    field: str
    operator: Operator
    value: Any


@dataclass
class Rule:
    id: str
    name: str
    conditions: List[Condition]
    match_type: str  # "all" or "any"
    actions: List[Dict[str, Any]]
    priority: int = 0
    enabled: bool = True


@dataclass
class EvaluationResult:
    rule_id: str
    matched: bool
    condition_results: List[Dict[str, Any]]


class RuleEngine:
    """Engine for evaluating rules against context."""
    
    OPERATORS = {
        Operator.EQ: operator.eq,
        Operator.NEQ: operator.ne,
        Operator.GT: operator.gt,
        Operator.GTE: operator.ge,
        Operator.LT: operator.lt,
        Operator.LTE: operator.le,
    }
    
    def __init__(self):
        self.rules: List[Rule] = []
    
    def add_rule(self, rule: Rule):
        """Add a rule to the engine."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)
    
    def load_rules(self, rules_config: List[Dict[str, Any]]):
        """Load rules from configuration."""
        for config in rules_config:
            conditions = [
                Condition(
                    field=c["field"],
                    operator=Operator(c["operator"]),
                    value=c["value"]
                )
                for c in config.get("conditions", [])
            ]
            
            rule = Rule(
                id=config.get("id", f"rule_{len(self.rules)}"),
                name=config["name"],
                conditions=conditions,
                match_type=config.get("match_type", "all"),
                actions=config.get("actions", []),
                priority=config.get("priority", 0),
                enabled=config.get("enabled", True),
            )
            self.add_rule(rule)
    
    def evaluate(self, context: Dict[str, Any]) -> Optional[Rule]:
        """
        Evaluate context against all rules.
        Returns the first matching rule (highest priority).
        """
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            result = self._evaluate_rule(rule, context)
            if result.matched:
                return rule
        
        return None
    
    def evaluate_all(self, context: Dict[str, Any]) -> List[Rule]:
        """Evaluate context and return all matching rules."""
        matching_rules = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            result = self._evaluate_rule(rule, context)
            if result.matched:
                matching_rules.append(rule)
        
        return matching_rules
    
    def _evaluate_rule(self, rule: Rule, context: Dict[str, Any]) -> EvaluationResult:
        """Evaluate a single rule against context."""
        condition_results = []
        
        for condition in rule.conditions:
            result = self._evaluate_condition(condition, context)
            condition_results.append({
                "field": condition.field,
                "operator": condition.operator.value,
                "expected": condition.value,
                "actual": self._get_field_value(context, condition.field),
                "matched": result,
            })
        
        if rule.match_type == "all":
            matched = all(r["matched"] for r in condition_results)
        else:  # "any"
            matched = any(r["matched"] for r in condition_results)
        
        return EvaluationResult(
            rule_id=rule.id,
            matched=matched,
            condition_results=condition_results,
        )
    
    def _evaluate_condition(self, condition: Condition, context: Dict[str, Any]) -> bool:
        """Evaluate a single condition."""
        actual_value = self._get_field_value(context, condition.field)
        
        if actual_value is None:
            return False
        
        op = condition.operator
        expected = condition.value
        
        if op in self.OPERATORS:
            return self.OPERATORS[op](actual_value, expected)
        
        if op == Operator.IN:
            return actual_value in expected
        
        if op == Operator.NOT_IN:
            return actual_value not in expected
        
        if op == Operator.CONTAINS:
            return expected in str(actual_value)
        
        if op == Operator.REGEX:
            return bool(re.match(expected, str(actual_value)))
        
        return False
    
    def _get_field_value(self, context: Dict[str, Any], field: str) -> Any:
        """Get nested field value from context using dot notation."""
        parts = field.split(".")
        value = context
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            else:
                return None
        
        return value


rule_engine = RuleEngine()
