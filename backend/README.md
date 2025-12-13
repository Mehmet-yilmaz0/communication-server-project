# Communication Server Backend

Flask backend for secure communication with encryption support.

## Project Structure

```
backend/
├── app.py                 # Flask application entry point
├── config.py              # Configuration (env variables)
├── database.py            # Database initialization
├── auth.py                # JWT authentication utilities
├── models/
│   ├── __init__.py
│   ├── user.py           # User model
│   └── message.py        # Message model (encrypted only)
├── routes/
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── messages.py       # Messages endpoints
│   └── crypto.py         # Crypto endpoints
└── services/
    ├── crypto_service.py  # Encryption/decryption service
    └── message_service.py # Message business logic
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `DATABASE_URL`: PostgreSQL connection string
   - `JWT_SECRET`: Secret key for JWT tokens (change in production!)

3. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE communication_db;
   ```

4. **Run the server:**
   ```bash
   python app.py
   ```
   
   Server will start on `http://localhost:5000`

## API Endpoints

### Authentication

**POST /api/auth/register**
- Register a new user
- Body: `{ "username": "user", "password": "pass" }`
- Returns: `{ "access_token": "...", "user": {...} }`

**POST /api/auth/login**
- Login user
- Body: `{ "username": "user", "password": "pass" }`
- Returns: `{ "access_token": "...", "user": {...} }`

### Messages

**GET /api/messages**
- Get all messages for authenticated user
- Headers: `Authorization: Bearer <token>`
- Returns: Array of message objects (encrypted content only, NOT decrypted)

**POST /api/messages**
- Send a new message
- Headers: `Authorization: Bearer <token>`
- Body: `{ "receiver_id": 2, "text": "HELLO", "method": "vigenere", "key": "KEY" }`
- Returns: Created message object (encrypted content only, NO plaintext)

**POST /api/messages/decrypt**
- Decrypt an encrypted message
- Body: `{ "encrypted": "RIJVS", "method": "vigenere", "key": "KEY" }`
- Returns: `{ "decrypted": "HELLO" }`
- Note: Does NOT save plaintext to database

### Crypto

**POST /api/crypto/encrypt**
- Encrypt text
- Body: `{ "text": "HELLO", "method": "vigenere", "key": "KEY" }`
- Returns: `{ "encrypted": "..." }`

**POST /api/crypto/decrypt**
- Decrypt text
- Body: `{ "text": "RIJVS", "method": "vigenere", "key": "KEY" }`
- Returns: `{ "decrypted": "HELLO" }`

## Supported Encryption Methods

- `vigenere`: Vigenère cipher (key: string)
- `caesar`: Caesar cipher (key: integer)
- `shift`: Shift cipher (key: integer)
- `playfair`: Playfair cipher (key: string)
- `hill`: Hill cipher (key: JSON matrix, e.g., `[[3,3],[2,5]]`)
- `rail_fence`: Rail fence cipher (key: integer, number of rails)
- `columnar_transposition`: Columnar transposition (key: string)
- `substitution`: Substitution cipher (key: string)
- `polybius`: Polybius cipher (key: string)
- `route`: Route cipher (key: string)
- `pigpen`: Pigpen cipher (key: string)

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Bcrypt hashed password
- `created_at`: Timestamp

### Message
- `id`: Primary key
- `sender_id`: Foreign key to users.id
- `receiver_id`: Foreign key to users.id
- `encryption_method`: Encryption method used
- `encrypted_content`: Encrypted message content (TEXT)
- `created_at`: Timestamp

**IMPORTANT**: Messages are stored **ONLY** in encrypted form. No plaintext is ever saved to the database.

## Security Features

- ✅ All messages encrypted before storage
- ✅ Plaintext never stored in database
- ✅ JWT authentication required for message operations
- ✅ Bcrypt password hashing
- ✅ CORS configured for frontend
- ✅ Error handling with meaningful messages

## Notes

- JWT tokens expire after 7 days
- CORS is configured for `http://localhost:3000`
- All encryption/decryption happens server-side
- Frontend must call `/api/messages/decrypt` to decrypt messages
