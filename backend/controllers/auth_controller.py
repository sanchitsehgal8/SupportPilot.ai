"""Auth Controller - authentication endpoints with Supabase integration"""
from flask import request, Blueprint
from functools import wraps
import uuid
from backend.utils.jwt_utils import JWTUtils
from backend.utils.validators import Validators
from backend.utils.error_handler import ErrorHandler
from backend.services.user_service import UserService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


class AuthController:
    """Handles authentication operations with Supabase integration"""
    
    def __init__(self, user_service: UserService, jwt_utils: JWTUtils, db=None):
        self.user_service = user_service
        self.jwt_utils = jwt_utils
        self.db = db
    
    def register(self, request_data: dict):
        """Register a new user with Supabase Auth and create user profile"""
        email = request_data.get('email', '').strip()
        password = request_data.get('password', '')
        name = request_data.get('name', '').strip()
        role = request_data.get('role', 'customer').lower()
        
        # Validate inputs
        valid, msg = Validators.validate_email(email)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_password(password)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_name(name)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        valid, msg = Validators.validate_user_role(role)
        if not valid:
            return ErrorHandler.bad_request(msg)
        
        # Check if user exists in database
        existing = self.user_service.get_user_by_email(email)
        if existing:
            return ErrorHandler.conflict('Email already registered')
        
        try:
            # In production: Use Supabase Auth to create user with password
            # For now, create user profile with generated user_id
            user_id = str(uuid.uuid4())
            
            result = self.user_service.create_user(user_id, email, name, role)
            
            if result['success']:
                # Generate JWT token
                token = self.jwt_utils.generate_token(user_id, email, role)
                return ErrorHandler.created_response({
                    'user_id': user_id,
                    'email': email,
                    'name': name,
                    'role': role,
                    'token': token
                }, 'User registered successfully')
            else:
                return ErrorHandler.internal_error(result.get('error'))
        except Exception as e:
            return ErrorHandler.internal_error(f'Registration failed: {str(e)}')
    
    def login(self, request_data: dict):
        """Login user and return JWT token"""
        email = request_data.get('email', '').strip()
        password = request_data.get('password', '')
        
        if not email or not password:
            return ErrorHandler.bad_request('Email and password required')
        
        try:
            # In production: Verify password against Supabase Auth
            # For demo: simple lookup and validation
            user = self.user_service.get_user_by_email(email)
            if not user:
                return ErrorHandler.unauthorized('Invalid credentials')
            
            if not user.get('is_active'):
                return ErrorHandler.forbidden('User account is inactive')
            
            # Generate JWT token
            token = self.jwt_utils.generate_token(
                user['user_id'],
                user['email'],
                user['role']
            )
            
            return ErrorHandler.success_response({
                'user_id': user['user_id'],
                'email': user['email'],
                'name': user['name'],
                'role': user['role'],
                'token': token
            }, 'Login successful')
        except Exception as e:
            return ErrorHandler.internal_error(f'Login failed: {str(e)}')
    
    def validate_token(self, token: str):
        """Validate JWT token and return payload"""
        payload = self.jwt_utils.decode_token(token)
        if payload is None:
            return None
        return payload
    
    def refresh_token(self, request_data: dict):
        """Refresh an expired token"""
        token = request_data.get('token', '').strip()
        
        if not token:
            return ErrorHandler.bad_request('Token required')
        
        new_token = self.jwt_utils.refresh_token(token)
        if not new_token:
            return ErrorHandler.unauthorized('Token refresh failed')
        
        payload = self.jwt_utils.decode_token(new_token)
        return ErrorHandler.success_response({
            'token': new_token,
            'user_id': payload['user_id'],
            'email': payload['email']
        }, 'Token refreshed')

    def create_agent(self, request_data: dict):
        """Create an agent user profile without returning an auth token.
        This is intended for admin workflows where issuing a token is not desired.
        """
        email = request_data.get('email', '').strip()
        password = request_data.get('password', '')
        name = request_data.get('name', '').strip()
        role = 'agent'

        # Validate inputs (reuse same validators)
        valid, msg = Validators.validate_email(email)
        if not valid:
            return ErrorHandler.bad_request(msg)

        valid, msg = Validators.validate_password(password)
        if not valid:
            return ErrorHandler.bad_request(msg)

        valid, msg = Validators.validate_name(name)
        if not valid:
            return ErrorHandler.bad_request(msg)

        # Check if user exists in database
        existing = self.user_service.get_user_by_email(email)
        if existing:
            return ErrorHandler.conflict('Email already registered')

        try:
            user_id = str(uuid.uuid4())
            result = self.user_service.create_user(user_id, email, name, role)
            if result['success']:
                # Return created user object WITHOUT token
                return ErrorHandler.created_response({
                    'user_id': user_id,
                    'email': email,
                    'name': name,
                    'role': role
                }, 'Agent created successfully')
            else:
                return ErrorHandler.internal_error(result.get('error'))
        except Exception as e:
            return ErrorHandler.internal_error(f'Create agent failed: {str(e)}')


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return ErrorHandler.unauthorized('Missing token')
        return f(*args, **kwargs)
    return decorated_function


def require_role(*roles):
    """Decorator to require specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                return ErrorHandler.unauthorized('Missing token')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
