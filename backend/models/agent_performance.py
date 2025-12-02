"""Agent Performance model class"""
from datetime import datetime
from typing import Dict


class AgentPerformance:
    """Represents performance metrics for a support agent"""
    
    def __init__(self, agent_id: str, tickets_resolved: int = 0,
                 average_response_time: float = 0.0,
                 average_resolution_time: float = 0.0,
                 customer_satisfaction_score: float = 0.0,
                 total_assigned_tickets: int = 0,
                 created_at: datetime = None, updated_at: datetime = None):
        self.agent_id = agent_id
        self.tickets_resolved = tickets_resolved
        self.average_response_time = average_response_time
        self.average_resolution_time = average_resolution_time
        self.customer_satisfaction_score = customer_satisfaction_score
        self.total_assigned_tickets = total_assigned_tickets
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'agent_id': self.agent_id,
            'tickets_resolved': self.tickets_resolved,
            'average_response_time': self.average_response_time,
            'average_resolution_time': self.average_resolution_time,
            'customer_satisfaction_score': self.customer_satisfaction_score,
            'total_assigned_tickets': self.total_assigned_tickets,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'AgentPerformance':
        """Create from dictionary"""
        return AgentPerformance(
            agent_id=data.get('agent_id'),
            tickets_resolved=data.get('tickets_resolved', 0),
            average_response_time=data.get('average_response_time', 0.0),
            average_resolution_time=data.get('average_resolution_time', 0.0),
            customer_satisfaction_score=data.get('customer_satisfaction_score', 0.0),
            total_assigned_tickets=data.get('total_assigned_tickets', 0)
        )
    
    def update_metrics(self, tickets_resolved: int, avg_response: float, 
                      avg_resolution: float, satisfaction: float, total: int):
        """Update all performance metrics"""
        self.tickets_resolved = tickets_resolved
        self.average_response_time = avg_response
        self.average_resolution_time = avg_resolution
        self.customer_satisfaction_score = satisfaction
        self.total_assigned_tickets = total
        self.updated_at = datetime.utcnow()
