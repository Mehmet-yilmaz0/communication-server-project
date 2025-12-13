"""
Crypto service to handle encryption/decryption using kriptoloji module
Supports all available cipher algorithms
"""
import sys
import os
import json

# Add parent directory to path to import kriptoloji
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from kriptoloji import (
    VigenereCipher, CaesarCipher, ShiftCipher,
    PlayfairCipher, HillCipher, RailFenceCipher,
    ColumnarTransposition, SubstitutionCipher,
    PolybiusCipher, RouteCipher, PigpenCipher
)

# Map method names to cipher instances
CIPHER_MAP = {
    'vigenere': VigenereCipher(),
    'caesar': CaesarCipher(),
    'shift': ShiftCipher(),
    'playfair': PlayfairCipher(),
    'hill': HillCipher(),
    'rail_fence': RailFenceCipher(),
    'columnar_transposition': ColumnarTransposition(),
    'substitution': SubstitutionCipher(),
    'polybius': PolybiusCipher(),
    'route': RouteCipher(),
    'pigpen': PigpenCipher(),
}

# Ciphers that require integer keys
INTEGER_KEY_CIPHERS = ['caesar', 'shift', 'rail_fence']

# Ciphers that require matrix keys
MATRIX_KEY_CIPHERS = ['hill']

# Ciphers that require string keys
STRING_KEY_CIPHERS = ['vigenere', 'playfair', 'columnar_transposition', 'substitution', 'polybius', 'route', 'pigpen']


def encrypt_text(text: str, method: str, key: str) -> str:
    """
    Encrypt text using specified method and key
    
    Args:
        text: Plain text to encrypt
        method: Encryption method (vigenere, caesar, hill, etc.)
        key: Encryption key (format depends on method)
    
    Returns:
        Encrypted text
    
    Raises:
        ValueError: If method is unsupported or key format is invalid
    """
    if method not in CIPHER_MAP:
        raise ValueError(f"Unsupported encryption method: {method}. Supported methods: {', '.join(CIPHER_MAP.keys())}")
    
    cipher = CIPHER_MAP[method]
    
    try:
        if method in INTEGER_KEY_CIPHERS:
            # Convert key to integer
            try:
                key_int = int(key) if isinstance(key, str) else key
                return cipher.encrypt(text, key_int)
            except ValueError:
                raise ValueError(f"Key for {method} must be an integer. Got: {key}")
        
        elif method in MATRIX_KEY_CIPHERS:
            # Parse key as JSON matrix
            try:
                if isinstance(key, str):
                    key_matrix = json.loads(key)
                else:
                    key_matrix = key
                return cipher.encrypt(text, key_matrix)
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Key for {method} must be a valid JSON matrix. Error: {str(e)}")
        
        else:
            # String key ciphers
            return cipher.encrypt(text, key)
    
    except Exception as e:
        raise ValueError(f"Encryption failed with {method}: {str(e)}")


def decrypt_text(text: str, method: str, key: str) -> str:
    """
    Decrypt text using specified method and key
    
    Args:
        text: Encrypted text to decrypt
        method: Decryption method (vigenere, caesar, hill, etc.)
        key: Decryption key (format depends on method)
    
    Returns:
        Decrypted text
    
    Raises:
        ValueError: If method is unsupported or key format is invalid
    """
    if method not in CIPHER_MAP:
        raise ValueError(f"Unsupported decryption method: {method}. Supported methods: {', '.join(CIPHER_MAP.keys())}")
    
    cipher = CIPHER_MAP[method]
    
    try:
        if method in INTEGER_KEY_CIPHERS:
            # Convert key to integer
            try:
                key_int = int(key) if isinstance(key, str) else key
                return cipher.decrypt(text, key_int)
            except ValueError:
                raise ValueError(f"Key for {method} must be an integer. Got: {key}")
        
        elif method in MATRIX_KEY_CIPHERS:
            # Parse key as JSON matrix
            try:
                if isinstance(key, str):
                    key_matrix = json.loads(key)
                else:
                    key_matrix = key
                return cipher.decrypt(text, key_matrix)
            except (json.JSONDecodeError, ValueError) as e:
                raise ValueError(f"Key for {method} must be a valid JSON matrix. Error: {str(e)}")
        
        else:
            # String key ciphers
            return cipher.decrypt(text, key)
    
    except Exception as e:
        raise ValueError(f"Decryption failed with {method}: {str(e)}")


def get_supported_methods():
    """Get list of supported encryption methods"""
    return list(CIPHER_MAP.keys())

