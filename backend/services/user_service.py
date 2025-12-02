"""User Service - handles user business logic"""
from typing import List, Dict, Optional
from datetime import datetime


class UserService:
    """Service class for user operations"""
    
    def __init__(self, db):
        self.db = db
        
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            result = self.db.table('users').select('*').eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            result = self.db.table('users').select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None
    
    def create_user(self, user_id: str, email: str, name: str, 
                   role: str = "customer") -> Dict:
        """Create a new user"""
        try:
            user_data = {
                'user_id': user_id,
                'email': email,
                'name': name,
                'role': role,
                'is_active': True,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('users').insert(user_data).execute()
            return {'success': True, 'data': result.data[0] if result.data else user_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_agents(self) -> List[Dict]:
        """Get all support agents"""
        try:
            result = self.db.table('users').select('*').eq('role', 'agent').execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def get_customers(self) -> List[Dict]:
        """Get all customers"""
        try:
            result = self.db.table('users').select('*').eq('role', 'customer').execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def update_user(self, user_id: str, updates: Dict) -> Dict:
        """Update user information"""
        try:
            updates['updated_at'] = datetime.utcnow().isoformat()
            result = self.db.table('users').update(updates).eq('user_id', user_id).execute()
            return {'success': True, 'data': result.data[0] if result.data else updates}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deactivate_user(self, user_id: str) -> Dict:
        """Deactivate a user"""
        return self.update_user(user_id, {'is_active': False})
