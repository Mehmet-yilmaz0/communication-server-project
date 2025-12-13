"""
Message service to handle message encryption and database operations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from models.message import Message
from services.crypto_service import encrypt_text, decrypt_text


def create_message(sender_id: int, receiver_id: int, plaintext: str, method: str, key: str) -> Message:
    """
    Create and save an encrypted message to database
    
    Args:
        sender_id: ID of the sender
        receiver_id: ID of the receiver
        plaintext: Plain text message to encrypt
        method: Encryption method
        key: Encryption key
    
    Returns:
        Created Message object
    
    Raises:
        ValueError: If encryption fails
    """
    # Encrypt the message using crypto service
    encrypted_content = encrypt_text(plaintext, method, key)
    
    # Create message with encrypted content only (NO plaintext stored)
    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        encryption_method=method,
        encrypted_content=encrypted_content
    )
    
    db.session.add(message)
    db.session.commit()
    
    return message


def get_user_messages(user_id: int):
    """
    Get all messages for a user (sent and received)
    
    Args:
        user_id: ID of the user
    
    Returns:
        List of Message objects (encrypted content only, NOT decrypted)
    """
    messages = Message.query.filter(
        (Message.sender_id == user_id) | (Message.receiver_id == user_id)
    ).order_by(Message.created_at.desc()).all()
    
    return messages


def decrypt_message_content(encrypted_content: str, method: str, key: str) -> str:
    """
    Decrypt message content (does NOT save to database)
    
    Args:
        encrypted_content: Encrypted text
        method: Decryption method
        key: Decryption key
    
    Returns:
        Decrypted plaintext
    
    Raises:
        ValueError: If decryption fails
    """
    return decrypt_text(encrypted_content, method, key)

