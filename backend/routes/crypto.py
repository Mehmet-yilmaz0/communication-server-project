"""
Crypto API routes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from services.crypto_service import encrypt_text, decrypt_text, get_methods_info

crypto_bp = Blueprint('crypto', __name__)


@crypto_bp.route('/api/crypto/encrypt', methods=['POST'])
def encrypt():
    """Encrypt text using specified method and key (key is optional for some algorithms)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        text = data.get('text')
        method = data.get('method')
        key = data.get('key')  # Optional for some algorithms
        
        if not text or not method:
            return jsonify({'error': 'text and method are required'}), 400
        
        # Key validation will be handled by encrypt_text function
        # Some algorithms don't require key (pigpen, caesar with default, polybius with standard matrix)
        encrypted = encrypt_text(text, method, key)
        
        return jsonify({'encrypted': encrypted}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@crypto_bp.route('/api/crypto/decrypt', methods=['POST'])
def decrypt():
    """Decrypt text using specified method and key (key is optional for some algorithms)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        text = data.get('text')
        method = data.get('method')
        key = data.get('key')  # Optional for some algorithms
        
        if not text or not method:
            return jsonify({'error': 'text and method are required'}), 400
        
        # Key validation will be handled by decrypt_text function
        # Some algorithms don't require key (pigpen, caesar with default, polybius with standard matrix)
        decrypted = decrypt_text(text, method, key)
        
        return jsonify({'decrypted': decrypted}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@crypto_bp.route('/api/crypto/methods', methods=['GET'])
def get_methods():
    """
    Get list of all supported encryption methods with their metadata.
    
    Returns:
        JSON array of method objects with:
        - id: Method identifier
        - label: Human-readable name
        - requires_key: Whether key is required (boolean)
        - hint: Optional hint about key format
    """
    try:
        methods = get_methods_info()
        return jsonify(methods), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

