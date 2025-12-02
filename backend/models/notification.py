"""Notification model class"""
from datetime import datetime
from typing import Dict, Optional


class Notification:
    """Represents a notification sent to a user"""
    
    def __init__(self, notification_id: str, user_id: str, title: str,
                 message: str, notification_type: str = "info",
                 related_ticket_id: Optional[str] = None,
                 is_read: bool = False, created_at: datetime = None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type  # 'info', 'alert', 'warning'
        self.related_ticket_id = related_ticket_id
        self.is_read = is_read
        self.created_at = created_at or datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'related_ticket_id': self.related_ticket_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Notification':
        """Create from dictionary"""
        return Notification(
            notification_id=data.get('notification_id'),
            user_id=data.get('user_id'),
            title=data.get('title'),
            message=data.get('message'),
            notification_type=data.get('notification_type', 'info'),
            related_ticket_id=data.get('related_ticket_id'),
            is_read=data.get('is_read', False)
        )
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
