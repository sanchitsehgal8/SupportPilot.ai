"""Audit Log model class"""
from datetime import datetime
from typing import Dict, Optional


class AuditLog:
    """Represents an audit log entry for tracking system actions"""
    
    def __init__(self, log_id: str, user_id: str, action: str,
                 entity_type: str, entity_id: str, changes: Dict = None,
                 ip_address: str = None, user_agent: str = None,
                 created_at: datetime = None):
        self.log_id = log_id
        self.user_id = user_id
        self.action = action
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.changes = changes or {}
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.created_at = created_at or datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'log_id': self.log_id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'changes': self.changes,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'AuditLog':
        """Create from dictionary"""
        return AuditLog(
            log_id=data.get('log_id'),
            user_id=data.get('user_id'),
            action=data.get('action'),
            entity_type=data.get('entity_type'),
            entity_id=data.get('entity_id'),
            changes=data.get('changes', {}),
            ip_address=data.get('ip_address'),
            user_agent=data.get('user_agent')
        )
