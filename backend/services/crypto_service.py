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


def encrypt_text(text: str, method: str, key: str = None) -> str:
    """
    Encrypt text using specified method and key
    
    Args:
        text: Plain text to encrypt
        method: Encryption method (vigenere, caesar, hill, etc.)
        key: Encryption key (format depends on method, optional for some algorithms)
    
    Returns:
        Encrypted text
    
    Raises:
        ValueError: If method is unsupported or key format is invalid
    """
    if method not in CIPHER_MAP:
        raise ValueError(f"Unsupported encryption method: {method}. Supported methods: {', '.join(CIPHER_MAP.keys())}")
    
    cipher = CIPHER_MAP[method]
    
    try:
        # Algorithms that don't require key
        if method == 'pigpen':
            # Pigpen doesn't use key
            return cipher.encrypt(text, None)
        
        if method in INTEGER_KEY_CIPHERS:
            # Convert key to integer
            # For caesar, if key is None, use default (3)
            if method == 'caesar' and (key is None or key == ''):
                return cipher.encrypt(text, None)  # Uses default key 3
            try:
                key_int = int(key) if isinstance(key, str) else key
                return cipher.encrypt(text, key_int)
            except (ValueError, TypeError):
                raise ValueError(f"Key for {method} must be an integer. Got: {key}")
        
        elif method in MATRIX_KEY_CIPHERS:
            # Parse key as JSON matrix
            if key is None or key == '':
                raise ValueError(f"Key is required for {method}")
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
            # For polybius, key can be None (uses standard matrix)
            if method == 'polybius' and (key is None or key == ''):
                return cipher.encrypt(text, None)
            # For other string key ciphers, key is required
            if key is None or key == '':
                raise ValueError(f"Key is required for {method}")
            return cipher.encrypt(text, key)
    
    except Exception as e:
        raise ValueError(f"Encryption failed with {method}: {str(e)}")


def decrypt_text(text: str, method: str, key: str = None) -> str:
    """
    Decrypt text using specified method and key
    
    Args:
        text: Encrypted text to decrypt
        method: Decryption method (vigenere, caesar, hill, etc.)
        key: Decryption key (format depends on method, optional for some algorithms)
    
    Returns:
        Decrypted text
    
    Raises:
        ValueError: If method is unsupported or key format is invalid
    """
    if method not in CIPHER_MAP:
        raise ValueError(f"Unsupported decryption method: {method}. Supported methods: {', '.join(CIPHER_MAP.keys())}")
    
    cipher = CIPHER_MAP[method]
    
    try:
        # Algorithms that don't require key
        if method == 'pigpen':
            # Pigpen doesn't use key
            return cipher.decrypt(text, None)
        
        if method in INTEGER_KEY_CIPHERS:
            # Convert key to integer
            # For caesar, if key is None, use default (3)
            if method == 'caesar' and (key is None or key == ''):
                return cipher.decrypt(text, None)  # Uses default key 3
            try:
                key_int = int(key) if isinstance(key, str) else key
                return cipher.decrypt(text, key_int)
            except (ValueError, TypeError):
                raise ValueError(f"Key for {method} must be an integer. Got: {key}")
        
        elif method in MATRIX_KEY_CIPHERS:
            # Parse key as JSON matrix
            if key is None or key == '':
                raise ValueError(f"Key is required for {method}")
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
            # For polybius, key can be None (uses standard matrix)
            if method == 'polybius' and (key is None or key == ''):
                return cipher.decrypt(text, None)
            # For other string key ciphers, key is required
            if key is None or key == '':
                raise ValueError(f"Key is required for {method}")
            return cipher.decrypt(text, key)
    
    except Exception as e:
        raise ValueError(f"Decryption failed with {method}: {str(e)}")


def get_supported_methods():
    """Get list of supported encryption methods"""
    return list(CIPHER_MAP.keys())


def get_methods_info():
    """
    Get detailed information about all supported encryption methods.
    
    Returns:
        List of dictionaries with method information:
        - id: Method identifier (e.g., 'vigenere')
        - label: Human-readable name (e.g., 'Vigenère Cipher')
        - requires_key: Whether key is required (True/False)
        - hint: Optional hint about key format
    """
    # Algoritma bilgileri
    methods_info = [
        {
            'id': 'vigenere',
            'label': 'Vigenère Cipher',
            'requires_key': True,
            'hint': 'Alphabetic key (e.g., "KEY")'
        },
        {
            'id': 'caesar',
            'label': 'Caesar Cipher',
            'requires_key': False,  # Default key is 3
            'hint': 'Integer shift (default: 3, optional)'
        },
        {
            'id': 'shift',
            'label': 'Shift Cipher',
            'requires_key': True,
            'hint': 'Integer shift (0-25)'
        },
        {
            'id': 'playfair',
            'label': 'Playfair Cipher',
            'requires_key': True,
            'hint': 'Alphabetic key (e.g., "MONARCHY")'
        },
        {
            'id': 'hill',
            'label': 'Hill Cipher',
            'requires_key': True,
            'hint': 'JSON matrix (e.g., [[3,3],[2,5]])'
        },
        {
            'id': 'rail_fence',
            'label': 'Rail Fence Cipher',
            'requires_key': True,
            'hint': 'Number of rails (integer, min: 2)'
        },
        {
            'id': 'columnar_transposition',
            'label': 'Columnar Transposition',
            'requires_key': True,
            'hint': 'Alphabetic key (e.g., "KEYWORD")'
        },
        {
            'id': 'substitution',
            'label': 'Substitution Cipher',
            'requires_key': True,
            'hint': '26-character permutation (e.g., "ZYXWVUTSRQPONMLKJIHGFEDCBA")'
        },
        {
            'id': 'polybius',
            'label': 'Polybius Square',
            'requires_key': False,  # Optional, uses standard matrix if not provided
            'hint': 'Alphabetic key (optional, uses standard matrix if empty)'
        },
        {
            'id': 'route',
            'label': 'Route Cipher',
            'requires_key': True,
            'hint': 'Format: "rows,cols,route" (e.g., "3,4,spiral_cw")'
        },
        {
            'id': 'pigpen',
            'label': 'Pigpen Cipher',
            'requires_key': False,  # Key not used in algorithm
            'hint': 'Key not required for this algorithm'
        },
    ]
    
    return methods_info
