"""
Event processing API endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

router = APIRouter()


class EventCreate(BaseModel):
    event_type: str
    source: str
    payload: Dict[str, Any]
    timestamp: Optional[datetime] = None


class EventResponse(BaseModel):
    event_id: str
    event_type: str
    source: str
    processed: bool
    decisions_triggered: List[str]
    received_at: datetime


@router.post("/", response_model=EventResponse)
async def receive_event(event: EventCreate):
    """
    Receive and process an event.
    
    Events trigger rule evaluation based on:
    - Event type
    - Event payload (context)
    
    Matching rules are evaluated and actions executed.
    """
    return {
        "event_id": "evt_abc123",
        "event_type": event.event_type,
        "source": event.source,
        "processed": True,
        "decisions_triggered": ["dec_xyz789"],
        "received_at": datetime.utcnow(),
    }


@router.get("/types")
async def list_event_types():
    """List configured event types and their rule mappings."""
    return {
        "event_types": [
            {"type": "lead.created", "rule_sets": ["lead_routing"]},
            {"type": "transaction.completed", "rule_sets": ["fraud_detection"]},
            {"type": "user.action", "rule_sets": ["engagement"]},
        ]
    }


@router.get("/history")
async def get_event_history(
    event_type: Optional[str] = None,
    source: Optional[str] = None,
    limit: int = 100,
):
    """Get event processing history."""
    return {"events": [], "total": 0}


@router.post("/replay/{event_id}")
async def replay_event(event_id: str):
    """Replay a historical event for testing."""
    return {
        "original_event_id": event_id,
        "replay_event_id": "evt_replay123",
        "status": "processed",
    }
