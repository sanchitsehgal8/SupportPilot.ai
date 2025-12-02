"""Error Handler - centralized error handling"""
from flask import jsonify
from typing import Tuple, Dict


class ErrorHandler:
    """Centralized error handling"""
    
    @staticmethod
    def handle_error(status_code: int, message: str, 
                    error_code: str = None) -> Tuple[Dict, int]:
        """Return standardized error response"""
        return {
            'success': False,
            'error': message,
            'error_code': error_code or 'UNKNOWN_ERROR'
        }, status_code
    
    @staticmethod
    def bad_request(message: str, error_code: str = 'BAD_REQUEST') -> Tuple[Dict, int]:
        """400 Bad Request"""
        return ErrorHandler.handle_error(400, message, error_code)
    
    @staticmethod
    def unauthorized(message: str = 'Unauthorized', 
                    error_code: str = 'UNAUTHORIZED') -> Tuple[Dict, int]:
        """401 Unauthorized"""
        return ErrorHandler.handle_error(401, message, error_code)
    
    @staticmethod
    def forbidden(message: str = 'Forbidden', 
                 error_code: str = 'FORBIDDEN') -> Tuple[Dict, int]:
        """403 Forbidden"""
        return ErrorHandler.handle_error(403, message, error_code)
    
    @staticmethod
    def not_found(message: str = 'Not Found', 
                 error_code: str = 'NOT_FOUND') -> Tuple[Dict, int]:
        """404 Not Found"""
        return ErrorHandler.handle_error(404, message, error_code)
    
    @staticmethod
    def conflict(message: str, error_code: str = 'CONFLICT') -> Tuple[Dict, int]:
        """409 Conflict"""
        return ErrorHandler.handle_error(409, message, error_code)
    
    @staticmethod
    def internal_error(message: str = 'Internal Server Error',
                      error_code: str = 'INTERNAL_ERROR') -> Tuple[Dict, int]:
        """500 Internal Server Error"""
        return ErrorHandler.handle_error(500, message, error_code)
    
    @staticmethod
    def success_response(data: Dict = None, message: str = 'Success') -> Tuple[Dict, int]:
        """200 Success response"""
        return {
            'success': True,
            'message': message,
            'data': data
        }, 200
    
    @staticmethod
    def created_response(data: Dict = None, message: str = 'Created') -> Tuple[Dict, int]:
        """201 Created response"""
        return {
            'success': True,
            'message': message,
            'data': data
        }, 201
