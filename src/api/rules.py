"""
Rules management API endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

router = APIRouter()


class Condition(BaseModel):
    field: str
    operator: str  # eq, neq, gt, gte, lt, lte, in, not_in, contains, regex
    value: Any


class Action(BaseModel):
    type: str
    config: Dict[str, Any] = {}


class RuleCreate(BaseModel):
    name: str
    description: str
    rule_set: str
    conditions: List[Condition]
    match_type: str = "all"  # all, any
    actions: List[Action]
    priority: int = 0
    enabled: bool = True


class RuleResponse(BaseModel):
    id: str
    name: str
    description: str
    rule_set: str
    priority: int
    enabled: bool
    created_at: datetime


@router.get("/", response_model=List[RuleResponse])
async def list_rules(rule_set: Optional[str] = None, enabled: Optional[bool] = None):
    """List all rules with optional filtering."""
    return []


@router.post("/", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(rule: RuleCreate):
    """
    Create a new decision rule.
    
    Rules consist of:
    - Conditions: criteria that must match
    - Match type: all (AND) or any (OR)
    - Actions: what to do when matched
    - Priority: higher priority rules evaluated first
    """
    return {
        "id": "rule_abc123",
        "name": rule.name,
        "description": rule.description,
        "rule_set": rule.rule_set,
        "priority": rule.priority,
        "enabled": rule.enabled,
        "created_at": datetime.utcnow(),
    }


@router.get("/{rule_id}", response_model=RuleResponse)
async def get_rule(rule_id: str):
    """Get rule by ID."""
    raise HTTPException(status_code=404, detail="Rule not found")


@router.put("/{rule_id}", response_model=RuleResponse)
async def update_rule(rule_id: str, rule: RuleCreate):
    """Update an existing rule."""
    return {
        "id": rule_id,
        "name": rule.name,
        "description": rule.description,
        "rule_set": rule.rule_set,
        "priority": rule.priority,
        "enabled": rule.enabled,
        "created_at": datetime.utcnow(),
    }


@router.delete("/{rule_id}")
async def delete_rule(rule_id: str):
    """Delete a rule."""
    return {"message": "Rule deleted", "rule_id": rule_id}


@router.post("/{rule_id}/test")
async def test_rule(rule_id: str, test_context: Dict[str, Any]):
    """Test a rule against sample context."""
    return {
        "rule_id": rule_id,
        "matched": True,
        "conditions_evaluated": [],
        "actions_would_execute": [],
    }


@router.get("/sets")
async def list_rule_sets():
    """List all rule sets."""
    return {
        "rule_sets": [
            {"name": "lead_routing", "rule_count": 5},
            {"name": "fraud_detection", "rule_count": 8},
            {"name": "pricing", "rule_count": 3},
        ]
    }
