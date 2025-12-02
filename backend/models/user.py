"""User model class"""
from datetime import datetime
from typing import Dict, List


class User:
    """Represents a system user (Admin, Agent, Customer)"""
    
    def __init__(self, user_id: str, email: str, name: str, role: str, 
                 created_at: datetime = None, updated_at: datetime = None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role  # 'admin', 'agent', 'customer'
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = True
        
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'User':
        """Create user from dictionary"""
        return User(
            user_id=data.get('user_id'),
            email=data.get('email'),
            name=data.get('name'),
            role=data.get('role', 'customer')
        )
