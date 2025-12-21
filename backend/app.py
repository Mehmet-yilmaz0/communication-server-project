"""
Flask application entry point
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database import db, init_db
from routes.auth import auth_bp
from routes.messages import messages_bp
from routes.crypto import crypto_bp
from routes.users import users_bp

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
init_db(app)

# CORS configuration
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(messages_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(users_bp)

# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
