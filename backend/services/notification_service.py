"""Notification Service - handles notifications"""
from typing import List, Dict, Optional
from datetime import datetime


class NotificationService:
    """Service class for notification operations"""
    
    def __init__(self, db):
        self.db = db
        
    def create_notification(self, user_id: str, title: str, message: str,
                          notification_type: str = "info",
                          related_ticket_id: Optional[str] = None) -> Dict:
        """Create and send a notification"""
        try:
            notification_data = {
                'user_id': user_id,
                'title': title,
                'message': message,
                'notification_type': notification_type,
                'related_ticket_id': related_ticket_id,
                'is_read': False,
                'created_at': datetime.utcnow().isoformat()
            }
            result = self.db.table('notifications').insert(notification_data).execute()
            return {'success': True, 'data': result.data[0] if result.data else notification_data}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_notifications(self, user_id: str, unread_only: bool = False) -> List[Dict]:
        """Get notifications for a user"""
        try:
            query = self.db.table('notifications').select('*').eq('user_id', user_id)
            if unread_only:
                query = query.eq('is_read', False)
            result = query.order('created_at', desc=True).execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def mark_as_read(self, notification_id: str) -> Dict:
        """Mark notification as read"""
        try:
            update_data = {'is_read': True}
            result = self.db.table('notifications').update(update_data).eq('notification_id', notification_id).execute()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def mark_all_as_read(self, user_id: str) -> Dict:
        """Mark all notifications for a user as read"""
        try:
            update_data = {'is_read': True}
            result = self.db.table('notifications').update(update_data).eq('user_id', user_id).eq('is_read', False).execute()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_notification(self, notification_id: str) -> Dict:
        """Delete a notification"""
        try:
            self.db.table('notifications').delete().eq('notification_id', notification_id).execute()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
