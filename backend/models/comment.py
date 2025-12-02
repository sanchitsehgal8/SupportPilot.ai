"""Comment model class"""
from datetime import datetime
from typing import Dict, Optional


class Comment:
    """Represents a comment on a ticket"""
    
    def __init__(self, comment_id: str, ticket_id: str, author_id: str,
                 content: str, is_internal: bool = False, 
                 created_at: datetime = None, updated_at: datetime = None):
        self.comment_id = comment_id
        self.ticket_id = ticket_id
        self.author_id = author_id
        self.content = content
        self.is_internal = is_internal
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert comment to dictionary"""
        return {
            'comment_id': self.comment_id,
            'ticket_id': self.ticket_id,
            'author_id': self.author_id,
            'content': self.content,
            'is_internal': self.is_internal,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Comment':
        """Create comment from dictionary"""
        return Comment(
            comment_id=data.get('comment_id'),
            ticket_id=data.get('ticket_id'),
            author_id=data.get('author_id'),
            content=data.get('content'),
            is_internal=data.get('is_internal', False)
        )
