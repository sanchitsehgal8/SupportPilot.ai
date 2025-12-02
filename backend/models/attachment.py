"""Attachment model class"""
from datetime import datetime
from typing import Dict


class Attachment:
    """Represents an attachment to a ticket or comment"""
    
    def __init__(self, attachment_id: str, ticket_id: str, author_id: str,
                 file_name: str, file_url: str, file_size: int,
                 mime_type: str, created_at: datetime = None):
        self.attachment_id = attachment_id
        self.ticket_id = ticket_id
        self.author_id = author_id
        self.file_name = file_name
        self.file_url = file_url
        self.file_size = file_size
        self.mime_type = mime_type
        self.created_at = created_at or datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert attachment to dictionary"""
        return {
            'attachment_id': self.attachment_id,
            'ticket_id': self.ticket_id,
            'author_id': self.author_id,
            'file_name': self.file_name,
            'file_url': self.file_url,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Attachment':
        """Create attachment from dictionary"""
        return Attachment(
            attachment_id=data.get('attachment_id'),
            ticket_id=data.get('ticket_id'),
            author_id=data.get('author_id'),
            file_name=data.get('file_name'),
            file_url=data.get('file_url'),
            file_size=data.get('file_size'),
            mime_type=data.get('mime_type')
        )
