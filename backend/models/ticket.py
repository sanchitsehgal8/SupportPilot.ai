"""Ticket model class"""
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class TicketStatus(Enum):
    """Ticket status enumeration"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(Enum):
    """Ticket priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Ticket:
    """Represents a customer support ticket"""
    
    def __init__(self, ticket_id: str, customer_id: str, title: str, 
                 description: str, priority: str = "medium", 
                 status: str = "open", assigned_agent_id: Optional[str] = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.ticket_id = ticket_id
        self.customer_id = customer_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.assigned_agent_id = assigned_agent_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.sentiment_score = None
        self.category = None
        self.tags: List[str] = []
        self.attachment_ids: List[str] = []
        
    def to_dict(self) -> Dict:
        """Convert ticket to dictionary"""
        return {
            'ticket_id': self.ticket_id,
            'customer_id': self.customer_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'assigned_agent_id': self.assigned_agent_id,
            'sentiment_score': self.sentiment_score,
            'category': self.category,
            'tags': self.tags,
            'attachment_ids': self.attachment_ids,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Ticket':
        """Create ticket from dictionary"""
        ticket = Ticket(
            ticket_id=data.get('ticket_id'),
            customer_id=data.get('customer_id'),
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'open'),
            assigned_agent_id=data.get('assigned_agent_id')
        )
        ticket.sentiment_score = data.get('sentiment_score')
        ticket.category = data.get('category')
        ticket.tags = data.get('tags', [])
        ticket.attachment_ids = data.get('attachment_ids', [])
        return ticket
    
    def assign_to_agent(self, agent_id: str):
        """Assign ticket to an agent"""
        self.assigned_agent_id = agent_id
        self.status = "in_progress"
        self.updated_at = datetime.utcnow()
    
    def close_ticket(self):
        """Close the ticket"""
        self.status = "closed"
        self.updated_at = datetime.utcnow()
    
    def resolve_ticket(self):
        """Mark ticket as resolved"""
        self.status = "resolved"
        self.updated_at = datetime.utcnow()
