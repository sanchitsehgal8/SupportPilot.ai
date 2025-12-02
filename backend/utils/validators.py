"""Validators - input validation utilities"""
import re
from typing import Tuple


class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain digit"
        return True, ""
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """Validate name"""
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters"
        if len(name) > 100:
            return False, "Name must not exceed 100 characters"
        return True, ""
    
    @staticmethod
    def validate_ticket_title(title: str) -> Tuple[bool, str]:
        """Validate ticket title"""
        if len(title.strip()) < 5:
            return False, "Title must be at least 5 characters"
        if len(title) > 200:
            return False, "Title must not exceed 200 characters"
        return True, ""
    
    @staticmethod
    def validate_ticket_description(description: str) -> Tuple[bool, str]:
        """Validate ticket description"""
        if len(description.strip()) < 10:
            return False, "Description must be at least 10 characters"
        if len(description) > 5000:
            return False, "Description must not exceed 5000 characters"
        return True, ""
    
    @staticmethod
    def validate_priority(priority: str) -> Tuple[bool, str]:
        """Validate ticket priority"""
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if priority not in valid_priorities:
            return False, f"Priority must be one of: {', '.join(valid_priorities)}"
        return True, ""
    
    @staticmethod
    def validate_user_role(role: str) -> Tuple[bool, str]:
        """Validate user role"""
        valid_roles = ['admin', 'agent', 'customer']
        if role not in valid_roles:
            return False, f"Role must be one of: {', '.join(valid_roles)}"
        return True, ""
