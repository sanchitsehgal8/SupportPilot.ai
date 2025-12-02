"""Analytics Controller - analytics endpoints"""
from flask import request, Blueprint
from backend.utils.error_handler import ErrorHandler
from backend.services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


class AnalyticsController:
    """Handles analytics operations"""
    
    def __init__(self, analytics_service: AnalyticsService):
        self.analytics_service = analytics_service
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        ticket_stats = self.analytics_service.get_ticket_statistics()
        sentiment_dist = self.analytics_service.get_sentiment_distribution()
        category_dist = self.analytics_service.get_category_distribution()
        response_metrics = self.analytics_service.get_response_time_metrics()
        
        return ErrorHandler.success_response({
            'tickets': ticket_stats,
            'sentiment': sentiment_dist,
            'categories': category_dist,
            'response_metrics': response_metrics
        })
    
    def get_agent_performance(self, agent_id: str):
        """Get performance metrics for an agent"""
        perf = self.analytics_service.get_agent_performance(agent_id)
        if not perf:
            return ErrorHandler.not_found('Agent performance data not found')
        return ErrorHandler.success_response(perf)
    
    def get_all_agents_performance(self):
        """Get performance for all agents"""
        agents_perf = self.analytics_service.get_all_agents_performance()
        return ErrorHandler.success_response({'agents': agents_perf})
    
    def get_sentiment_analytics(self):
        """Get sentiment distribution"""
        sentiment = self.analytics_service.get_sentiment_distribution()
        return ErrorHandler.success_response(sentiment)
    
    def get_response_time_analytics(self):
        """Get response time metrics"""
        days = request.args.get('days', 30, type=int)
        metrics = self.analytics_service.get_response_time_metrics(days)
        return ErrorHandler.success_response(metrics)
    
    def get_category_analytics(self):
        """Get category distribution"""
        categories = self.analytics_service.get_category_distribution()
        return ErrorHandler.success_response(categories)
