"""SupportPilot Flask Application with Supabase and JWT Auth"""
import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv

# Ensure backend module is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from root directory
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, '.env'))

# Import configuration and components
from backend.config import get_config
from backend.utils.supabase_client import SupabaseClient
from backend.utils.jwt_utils import JWTUtils
from backend.utils.error_handler import ErrorHandler
from backend.services.user_service import UserService
from backend.services.ticket_service import TicketService
from backend.services.comment_service import CommentService
from backend.services.notification_service import NotificationService
from backend.services.analytics_service import AnalyticsService
from backend.services.assignment_engine import TicketAssignmentEngine
from backend.controllers.auth_controller import AuthController
from backend.controllers.ticket_controller import TicketController
from backend.controllers.analytics_controller import AnalyticsController


def create_app():
    """Application factory with full initialization"""
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    
    # Initialize Supabase
    db = None
    try:
        supabase_url = os.getenv('SUPABASE_URL', '').strip()
        supabase_key = os.getenv('SUPABASE_KEY', '').strip()
        
        if supabase_url and supabase_key:
            supabase_client = SupabaseClient(supabase_url, supabase_key)
            db = supabase_client.get_client()
            print("✓ Supabase connected")
        else:
            print("⚠  Supabase credentials missing — running in demo mode")
    except Exception as e:
        print(f"⚠  Supabase error: {e} — continuing in demo mode")
        import traceback
        traceback.print_exc()
    
    # Initialize JWT
    jwt_secret = os.getenv('JWT_SECRET_KEY', app.config['JWT_SECRET_KEY'])
    jwt_utils = JWTUtils(jwt_secret)
    
    # Initialize services (graceful degradation if db unavailable)
    user_service = UserService(db) if db else None
    ticket_service = TicketService(db) if db else None
    comment_service = CommentService(db) if db else None
    notification_service = NotificationService(db) if db else None
    analytics_service = AnalyticsService(db) if db else None
    assignment_engine = TicketAssignmentEngine(db, user_service, analytics_service) if db and user_service else None
    
    # Initialize controllers
    auth_controller = AuthController(user_service, jwt_utils, db) if user_service else None
    ticket_controller = TicketController(ticket_service) if ticket_service else None
    analytics_controller = AnalyticsController(analytics_service) if analytics_service else None
    
    # ===== MIDDLEWARE =====
    
    def require_auth(f):
        """JWT authentication decorator"""
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.headers.get('Authorization', '')
            if not auth.startswith('Bearer '):
                return ErrorHandler.unauthorized('Missing Authorization header')
            token = auth[7:]
            payload = jwt_utils.decode_token(token)
            if not payload:
                return ErrorHandler.unauthorized('Invalid or expired token')
            request.user = payload
            return f(*args, **kwargs)
        return decorated
    
    def require_role(*roles):
        """Role-based access control decorator"""
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if not hasattr(request, 'user') or request.user.get('role') not in roles:
                    return ErrorHandler.forbidden('Insufficient permissions')
                return f(*args, **kwargs)
            return decorated
        return decorator
    
    # ===== AUTH ROUTES =====
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        if not auth_controller:
            return ErrorHandler.internal_error('Auth service unavailable')
        return auth_controller.register(request.get_json() or {})

    @app.route('/api/auth/create-agent', methods=['POST'])
    @require_auth
    @require_role('admin')
    def create_agent():
        if not auth_controller:
            return ErrorHandler.internal_error('Auth service unavailable')
        return auth_controller.create_agent(request.get_json() or {})
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        if not auth_controller:
            return ErrorHandler.internal_error('Auth service unavailable')
        return auth_controller.login(request.get_json() or {})
    
    @app.route('/api/auth/validate', methods=['GET'])
    @require_auth
    def validate():
        return ErrorHandler.success_response({
            'user_id': request.user['user_id'],
            'email': request.user['email'],
            'role': request.user['role']
        }, 'Valid')
    
    @app.route('/api/auth/refresh', methods=['POST'])
    def refresh():
        if not auth_controller:
            return ErrorHandler.internal_error('Auth service unavailable')
        return auth_controller.refresh_token(request.get_json() or {})
    
    # ===== TICKET ROUTES =====
    
    @app.route('/api/tickets', methods=['POST'])
    @require_auth
    def create_ticket():
        if not ticket_controller:
            return ErrorHandler.internal_error('Ticket service unavailable')
        return ticket_controller.create_ticket(request.get_json() or {}, request.user['user_id'])
    
    @app.route('/api/tickets', methods=['GET'])
    @require_auth
    def list_tickets():
        if not ticket_controller:
            return ErrorHandler.internal_error('Ticket service unavailable')
        
        if request.user['role'] == 'customer':
            return ticket_controller.get_my_tickets(request.user['user_id'])
        elif request.user['role'] == 'agent':
            return ticket_controller.get_assigned_tickets(request.user['user_id'])
        else:  # admin
            limit = request.args.get('limit', 50, type=int)
            offset = request.args.get('offset', 0, type=int)
            return ticket_controller.get_all_tickets({'limit': limit, 'offset': offset})
    
    @app.route('/api/tickets/<ticket_id>', methods=['GET'])
    @require_auth
    def get_ticket(ticket_id):
        if not ticket_controller:
            return ErrorHandler.internal_error('Ticket service unavailable')
        return ticket_controller.get_ticket(ticket_id)
    
    @app.route('/api/tickets/<ticket_id>/status', methods=['PUT'])
    @require_auth
    @require_role('agent', 'admin')
    def update_status(ticket_id):
        if not ticket_controller:
            return ErrorHandler.internal_error('Ticket service unavailable')
        return ticket_controller.update_ticket_status(ticket_id, request.get_json() or {})
    
    @app.route('/api/tickets/<ticket_id>/assign', methods=['POST'])
    @require_auth
    @require_role('admin', 'agent')
    def assign(ticket_id):
        if not ticket_controller:
            return ErrorHandler.internal_error('Ticket service unavailable')
        return ticket_controller.assign_ticket(ticket_id, request.get_json() or {})
    
    # ===== COMMENT ROUTES =====
    
    @app.route('/api/tickets/<ticket_id>/comments', methods=['POST'])
    @require_auth
    def add_comment(ticket_id):
        if not comment_service:
            return ErrorHandler.internal_error('Comment service unavailable')
        
        data = request.get_json() or {}
        content = data.get('content', '').strip()
        is_internal = data.get('is_internal', False)
        
        if not content:
            return ErrorHandler.bad_request('Content required')
        
        result = comment_service.create_comment(ticket_id, request.user['user_id'], content, is_internal)
        return ErrorHandler.created_response(result.get('data')) if result.get('success') else ErrorHandler.internal_error(result.get('error'))
    
    @app.route('/api/tickets/<ticket_id>/comments', methods=['GET'])
    @require_auth
    def list_comments(ticket_id):
        if not comment_service:
            return ErrorHandler.internal_error('Comment service unavailable')
        comments = comment_service.get_ticket_comments(ticket_id)
        return ErrorHandler.success_response({'comments': comments})
    
    # ===== ANALYTICS ROUTES =====
    
    @app.route('/api/analytics/dashboard', methods=['GET'])
    @require_auth
    @require_role('admin', 'agent')
    def dashboard():
        if not analytics_controller:
            return ErrorHandler.internal_error('Analytics service unavailable')
        return analytics_controller.get_dashboard_stats()
    
    @app.route('/api/analytics/agents', methods=['GET'])
    @require_auth
    @require_role('admin')
    def list_agents():
        if not analytics_controller:
            return ErrorHandler.internal_error('Analytics service unavailable')
        return analytics_controller.get_all_agents_performance()

    @app.route('/api/users/agents', methods=['GET'])
    @require_auth
    @require_role('admin')
    def list_user_agents():
        if not user_service:
            return ErrorHandler.internal_error('User service unavailable')
        try:
            agents = user_service.get_agents()
            return ErrorHandler.success_response({'agents': agents})
        except Exception as e:
            return ErrorHandler.internal_error(str(e))
    
    @app.route('/api/analytics/agents/<agent_id>', methods=['GET'])
    @require_auth
    def agent_stats(agent_id):
        if not analytics_controller:
            return ErrorHandler.internal_error('Analytics service unavailable')
        return analytics_controller.get_agent_performance(agent_id)
    
    # ===== HEALTH CHECK =====
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return ErrorHandler.success_response({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected' if db else 'demo_mode'
        })
    
    # ===== ERROR HANDLERS =====
    
    @app.errorhandler(404)
    def not_found(error):
        return ErrorHandler.not_found('Endpoint not found')
    
    @app.errorhandler(500)
    def server_error(error):
        app.logger.error(f"Server error: {error}")
        return ErrorHandler.internal_error()
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SupportPilot Flask Server")
    print("="*60)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Supabase: {'Enabled' if os.getenv('SUPABASE_URL') else 'Disabled (demo mode)'}")
    api_port = os.getenv('PORT', '5001')
    print(f"API: http://localhost:{api_port}/api")
    print("="*60 + "\n")

    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            use_reloader=False
        )
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
