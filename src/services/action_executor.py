"""
Action executor for running decision actions.
"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod
import structlog

logger = structlog.get_logger()


class BaseAction(ABC):
    """Base class for actions."""
    
    @abstractmethod
    async def execute(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the action."""
        pass


class AssignAction(BaseAction):
    """Action to assign something to a team/person."""
    
    async def execute(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        assignee = config.get("to")
        logger.info("Assigning", assignee=assignee, context_id=context.get("id"))
        return {"assigned_to": assignee, "success": True}


class NotifyAction(BaseAction):
    """Action to send notifications."""
    
    async def execute(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        channel = config.get("channel", "email")
        message = config.get("message", "Notification")
        logger.info("Notifying", channel=channel, message=message)
        return {"channel": channel, "sent": True}


class WebhookAction(BaseAction):
    """Action to call external webhook."""
    
    async def execute(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        url = config.get("url")
        logger.info("Calling webhook", url=url)
        # Would make HTTP call here
        return {"url": url, "status_code": 200}


class FlagAction(BaseAction):
    """Action to flag/mark something."""
    
    async def execute(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        severity = config.get("severity", "medium")
        reason = config.get("reason", "Rule matched")
        logger.info("Flagging", severity=severity, reason=reason)
        return {"flagged": True, "severity": severity}


class ActionExecutor:
    """Executor for running decision actions."""
    
    def __init__(self):
        self.actions: Dict[str, BaseAction] = {
            "assign": AssignAction(),
            "notify": NotifyAction(),
            "webhook": WebhookAction(),
            "flag": FlagAction(),
        }
    
    def register_action(self, action_type: str, action: BaseAction):
        """Register a custom action type."""
        self.actions[action_type] = action
    
    async def execute(
        self,
        actions: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Execute a list of actions."""
        results = []
        
        for action_config in actions:
            action_type = action_config.get("type")
            config = action_config.get("config", {})
            
            if action_type not in self.actions:
                results.append({
                    "type": action_type,
                    "success": False,
                    "error": f"Unknown action type: {action_type}",
                })
                continue
            
            try:
                action = self.actions[action_type]
                result = await action.execute(config, context)
                results.append({
                    "type": action_type,
                    "success": True,
                    "result": result,
                })
            except Exception as e:
                results.append({
                    "type": action_type,
                    "success": False,
                    "error": str(e),
                })
        
        return results


action_executor = ActionExecutor()
