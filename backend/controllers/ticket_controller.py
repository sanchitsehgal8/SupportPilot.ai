"""Ticket Controller - ticket management endpoints"""
from flask import request, Blueprint
from backend.utils.validators import Validators
from backend.utils.error_handler import ErrorHandler
from backend.services.ticket_service import TicketService
from backend.ml.predictor import SentimentAnalyzer, PriorityPredictor, KeywordExtractor

ticket_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')


class TicketController:
    """Handles ticket operations"""
    
    def __init__(self, ticket_service: TicketService):
        self.ticket_service = ticket_service
        self.sentiment_analyzer = SentimentAnalyzer()
        self.priority_predictor = PriorityPredictor()
        self.keyword_extractor = KeywordExtractor()
    
    def create_ticket(self, request_data: dict, customer_id: str):
        """Create a new ticket"""
        title = request_data.get('title', '').strip()
        description = request_data.get('description', '').strip()
        priority = request_data.get('priority', 'medium').lower()
        
        # Validate inputs
        valid, msg = Validators.validate_ticket_title(title)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_ticket_description(description)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_priority(priority)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        # ML: Analyze sentiment and predict priority
        sentiment = self.sentiment_analyzer.analyze(description)
        predicted_priority = self.priority_predictor.predict_priority(
            description, sentiment['score']
        )
        keywords = self.keyword_extractor.extract(description)
        
        # Create ticket
        result = self.ticket_service.create_ticket(
            customer_id, title, description, priority
        )
        
        if result['success']:
            # Update with ML results
            ticket = result['data']
            ticket['sentiment_score'] = sentiment['score']
            ticket['sentiment_label'] = sentiment['label']
            ticket['predicted_priority'] = predicted_priority
            ticket['keywords'] = keywords
            
            return ErrorHandler.created_response(ticket, 'Ticket created successfully')
        else:
            return ErrorHandler.internal_error(result.get('error'))
    
    def get_ticket(self, ticket_id: str):
        """Get ticket details"""
        ticket = self.ticket_service.get_ticket(ticket_id)
        if not ticket:
            return ErrorHandler.not_found('Ticket not found')
        return ErrorHandler.success_response(ticket)
    
    def get_my_tickets(self, customer_id: str):
        """Get all tickets for customer"""
        tickets = self.ticket_service.get_customer_tickets(customer_id)
        return ErrorHandler.success_response({'tickets': tickets})
    
    def get_assigned_tickets(self, agent_id: str):
        """Get assigned tickets for agent"""
        tickets = self.ticket_service.get_agent_tickets(agent_id)
        return ErrorHandler.success_response({'tickets': tickets})
    
    def update_ticket_status(self, ticket_id: str, request_data: dict):
        """Update ticket status"""
        status = request_data.get('status', '').lower()
        
        valid_statuses = ['open', 'in_progress', 'pending', 'resolved', 'closed']
        if status not in valid_statuses:
            return ErrorHandler.bad_request(f'Invalid status: {status}')
        
        result = self.ticket_service.update_ticket_status(ticket_id, status)
        
        if result['success']:
            return ErrorHandler.success_response(result['data'], 'Status updated')
        else:
            return ErrorHandler.internal_error(result.get('error'))
    
    def assign_ticket(self, ticket_id: str, request_data: dict):
        """Assign ticket to agent"""
        agent_id = request_data.get('agent_id', '').strip()
        
        if not agent_id:
            return ErrorHandler.bad_request('Agent ID required')
        
        result = self.ticket_service.assign_ticket(ticket_id, agent_id)
        
        if result['success']:
            return ErrorHandler.success_response(result['data'], 'Ticket assigned')
        else:
            return ErrorHandler.internal_error(result.get('error'))
    
    def get_all_tickets(self, request_data: dict = None):
        """Get all tickets with pagination"""
        limit = request_data.get('limit', 50) if request_data else 50
        offset = request_data.get('offset', 0) if request_data else 0
        
        tickets = self.ticket_service.get_all_tickets(limit, offset)
        return ErrorHandler.success_response({'tickets': tickets})
