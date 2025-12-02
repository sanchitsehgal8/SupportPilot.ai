"""Analytics Service - handles analytics and metrics"""
from typing import Dict, List
from datetime import datetime, timedelta


class AnalyticsService:
    """Service class for analytics operations"""
    
    def __init__(self, db):
        self.db = db
        
    def get_ticket_statistics(self) -> Dict:
        """Get overall ticket statistics"""
        try:
            tickets = self.db.table('tickets').select('status, priority').execute()
            data = tickets.data if tickets.data else []
            
            stats = {
                'total_tickets': len(data),
                'open_tickets': len([t for t in data if t.get('status') == 'open']),
                'in_progress_tickets': len([t for t in data if t.get('status') == 'in_progress']),
                'resolved_tickets': len([t for t in data if t.get('status') == 'resolved']),
                'closed_tickets': len([t for t in data if t.get('status') == 'closed']),
                'high_priority': len([t for t in data if t.get('priority') == 'high']),
                'urgent_tickets': len([t for t in data if t.get('priority') == 'urgent'])
            }
            return stats
        except Exception as e:
            return {}
    
    def get_agent_performance(self, agent_id: str) -> Dict:
        """Get performance metrics for an agent"""
        try:
            perf = self.db.table('agent_performance').select('*').eq('agent_id', agent_id).execute()
            return perf.data[0] if perf.data else {}
        except Exception as e:
            return {}
    
    def get_all_agents_performance(self) -> List[Dict]:
        """Get performance for all agents"""
        try:
            result = self.db.table('agent_performance').select('*').execute()
            return result.data if result.data else []
        except Exception as e:
            return []
    
    def get_sentiment_distribution(self) -> Dict:
        """Get distribution of ticket sentiments"""
        try:
            tickets = self.db.table('tickets').select('sentiment_score').execute()
            data = tickets.data if tickets.data else []
            
            positive = len([t for t in data if t.get('sentiment_score', 0) > 0.5])
            neutral = len([t for t in data if 0.3 <= t.get('sentiment_score', 0) <= 0.5])
            negative = len([t for t in data if t.get('sentiment_score', 0) < 0.3])
            
            return {
                'positive': positive,
                'neutral': neutral,
                'negative': negative
            }
        except Exception as e:
            return {}
    
    def get_response_time_metrics(self, days: int = 30) -> Dict:
        """Get average response time metrics"""
        try:
            since_date = (datetime.utcnow() - timedelta(days=days)).isoformat()
            tickets = self.db.table('tickets').select('*').gte('created_at', since_date).execute()
            data = tickets.data if tickets.data else []
            
            total_response_times = sum([t.get('response_time', 0) for t in data])
            avg_response = total_response_times / len(data) if len(data) > 0 else 0
            
            return {
                'average_response_time_hours': avg_response / 3600,
                'total_tickets_period': len(data)
            }
        except Exception as e:
            return {}
    
    def get_category_distribution(self) -> Dict:
        """Get distribution of ticket categories"""
        try:
            tickets = self.db.table('tickets').select('category').execute()
            data = tickets.data if tickets.data else []
            
            categories = {}
            for ticket in data:
                cat = ticket.get('category', 'uncategorized')
                categories[cat] = categories.get(cat, 0) + 1
            
            return categories
        except Exception as e:
            return {}
