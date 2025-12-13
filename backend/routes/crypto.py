"""
Crypto API routes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from services.crypto_service import encrypt_text, decrypt_text

crypto_bp = Blueprint('crypto', __name__)


@crypto_bp.route('/api/crypto/encrypt', methods=['POST'])
def encrypt():
    """Encrypt text using specified method and key"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        text = data.get('text')
        method = data.get('method')
        key = data.get('key')
        
        if not text or not method or not key:
            return jsonify({'error': 'text, method, and key are required'}), 400
        
        encrypted = encrypt_text(text, method, key)
        
        return jsonify({'encrypted': encrypted}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@crypto_bp.route('/api/crypto/decrypt', methods=['POST'])
def decrypt():
    """Decrypt text using specified method and key"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        text = data.get('text')
        method = data.get('method')
        key = data.get('key')
        
        if not text or not method or not key:
            return jsonify({'error': 'text, method, and key are required'}), 400
        
        decrypted = decrypt_text(text, method, key)
        
        return jsonify({'decrypted': decrypted}), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

