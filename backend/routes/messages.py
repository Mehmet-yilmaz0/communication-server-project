"""
Messages API routes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from database import db
from auth import require_auth
from services.message_service import create_message, get_user_messages, decrypt_message_content
from services.crypto_service import decrypt_text

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/api/messages', methods=['GET'])
@require_auth
def get_messages():
    """
    Get all messages for the current user
    
    Returns encrypted content only, NOT decrypted.
    Frontend should decrypt using /api/messages/decrypt endpoint.
    """
    try:
        user_id = request.current_user_id
        
        # Get messages (encrypted content only)
        messages = get_user_messages(user_id)
        
        # Return messages with encrypted content (NO plaintext)
        return jsonify([msg.to_dict() for msg in messages]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/api/messages', methods=['POST'])
@require_auth
def send_message():
    """
    Send a new message
    
    Request body:
    {
        "receiver_id": 2,
        "text": "HELLO",
        "method": "vigenere",
        "key": "KEY"
    }
    
    Response:
    {
        "id": 10,
        "encrypted_content": "RIJVS",
        "method": "vigenere",
        "created_at": "2025-01-10T21:00:00Z"
    }
    
    Note: Plaintext is NOT returned in response, only encrypted content.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        receiver_id = data.get('receiver_id')
        text = data.get('text')
        method = data.get('method')
        key = data.get('key')  # Optional for some algorithms
        
        # Validate required fields
        if not receiver_id or not text or not method:
            return jsonify({
                'error': 'receiver_id, text, and method are required'
            }), 400
        
        # Key validation will be handled by create_message function
        # Some algorithms don't require key (pigpen, caesar with default, polybius with standard matrix)
        
        sender_id = request.current_user_id
        
        # Create message (encrypts and saves to DB)
        # Plaintext is NEVER stored in database
        message = create_message(sender_id, receiver_id, text, method, key)
        
        # Return message with encrypted content only (NO plaintext)
        return jsonify(message.to_dict()), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@messages_bp.route('/api/messages/decrypt', methods=['POST'])
def decrypt_message():
    """
    Decrypt an encrypted message
    
    Request body:
    {
        "encrypted": "RIJVS",
        "method": "vigenere",
        "key": "KEY"
    }
    
    Response:
    {
        "decrypted": "HELLO"
    }
    
    Note: This does NOT save plaintext to database.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        encrypted = data.get('encrypted')
        method = data.get('method')
        key = data.get('key')
        
        if not encrypted or not method or not key:
            return jsonify({
                'error': 'encrypted, method, and key are required'
            }), 400
        
        # Decrypt using crypto service
        # Plaintext is NOT saved to database
        decrypted = decrypt_text(encrypted, method, key)
        
        return jsonify({'decrypted': decrypted}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 400

