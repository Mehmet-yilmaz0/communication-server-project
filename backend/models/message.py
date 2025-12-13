"""
Message model
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from datetime import datetime

class Message(db.Model):
    """Message model - stores only encrypted content"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    encryption_method = db.Column(db.String(50), nullable=False)  # vigenere, caesar, hill, etc.
    encrypted_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # NO plaintext field - messages are stored encrypted only
    
    def to_dict(self):
        """Convert message to dictionary - returns encrypted content only"""
        return {
            'id': self.id,
            'encrypted_content': self.encrypted_content,
            'method': self.encryption_method,
            'created_at': self.created_at.isoformat() + 'Z',
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id
        }

