"""Comment Service - handles comment operations"""
from typing import List, Dict
from datetime import datetime
import uuid


class CommentService:
    """Service class for comment operations"""
    
    def __init__(self, db):
        self.db = db
        
    def create_comment(self, ticket_id: str, author_id: str, content: str,
                      is_internal: bool = False) -> Dict:
        """Create a new comment"""
        try:
            comment_id = str(uuid.uuid4())
            comment_data = {
                'comment_id': comment_id,
                'ticket_id': ticket_id,
                'author_id': author_id,
                'content': content,
                'is_internal': is_internal,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('comments').insert(comment_data).execute()
            return {'success': True, 'data': result.data[0] if result.data else comment_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_ticket_comments(self, ticket_id: str) -> List[Dict]:
        """Get all comments for a ticket"""
        try:
            result = self.db.table('comments').select('*').eq('ticket_id', ticket_id).order('created_at', desc=False).execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def get_comment(self, comment_id: str) -> Dict:
        """Get comment by ID"""
        try:
            result = self.db.table('comments').select('*').eq('comment_id', comment_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None
    
    def update_comment(self, comment_id: str, content: str) -> Dict:
        """Update comment content"""
        try:
            update_data = {
                'content': content,
                'updated_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('comments').update(update_data).eq('comment_id', comment_id).execute()
            return {'success': True, 'data': result.data[0] if result.data else update_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_comment(self, comment_id: str) -> Dict:
        """Delete a comment"""
        try:
            result = self.db.table('comments').delete().eq('comment_id', comment_id).execute()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
