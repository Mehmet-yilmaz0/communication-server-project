"""
Users API routes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from database import db
from models.user import User
from auth import require_auth

users_bp = Blueprint('users', __name__)


@users_bp.route('/api/users', methods=['GET'])
@require_auth
def get_users():
    """
    Get all users except the currently logged-in user.
    
    Returns:
        JSON array of user objects with id and username
        Example: [{"id": 2, "username": "alice"}, {"id": 3, "username": "bob"}]
    """
    try:
        current_user_id = request.current_user_id
        
        # Get all users except the current user
        users = User.query.filter(User.id != current_user_id).all()
        
        # Convert to dictionary format
        users_list = [user.to_dict() for user in users]
        
        return jsonify(users_list), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

