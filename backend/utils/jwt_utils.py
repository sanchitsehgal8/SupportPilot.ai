"""JWT Utilities - JWT token handling"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional


class JWTUtils:
    """Utilities for JWT token generation and validation"""
    
    def __init__(self, secret_key: str, algorithm: str = 'HS256'):
        self.secret_key = secret_key
        self.algorithm = algorithm
        
    def generate_token(self, user_id: str, email: str, role: str,
                      expires_in_hours: int = 24) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours)
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def decode_token(self, token: str) -> Optional[Dict]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_token(self, token: str, expires_in_hours: int = 24) -> Optional[str]:
        """Refresh an existing token"""
        payload = self.decode_token(token)
        if payload is None:
            return None
        
        return self.generate_token(
            payload['user_id'],
            payload['email'],
            payload['role'],
            expires_in_hours
        )
    
    def get_user_id_from_token(self, token: str) -> Optional[str]:
        """Extract user_id from token"""
        payload = self.decode_token(token)
        return payload['user_id'] if payload else None
    
    def get_role_from_token(self, token: str) -> Optional[str]:
        """Extract role from token"""
        payload = self.decode_token(token)
        return payload['role'] if payload else None
