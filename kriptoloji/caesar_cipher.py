"""
Caesar Cipher (Sezar Şifresi)
Shift Cipher'ın özel bir durumu. Key her zaman 3'tür.

Algoritma:
Shift Cipher ile aynı, ancak key sabit olarak 3'tür.
Klasik Caesar Cipher: her harfi 3 pozisyon ileri kaydırır.

Örnek:
A -> D
B -> E
C -> F
...
X -> A (döngü)
Y -> B
Z -> C
"""

from .shift_cipher import ShiftCipher


class CaesarCipher:
    """
    Caesar Cipher implementasyonu.
    Shift Cipher'ı key=3 ile kullanır.
    """
    
    def __init__(self):
        self.shift_cipher = ShiftCipher()
        self.default_key = 3  # Klasik Caesar shift
    
    def encrypt(self, plaintext: str, key: int = None) -> str:
        """
        Metni Caesar Cipher ile şifreler.
        
        Args:
            plaintext: Şifrelenecek metin
            key: Kaydırma miktarı (varsayılan: 3, klasik Caesar)
        
        Returns:
            Şifreli metin
        """
        if key is None:
            key = self.default_key
        return self.shift_cipher.encrypt(plaintext, key)
    
    def decrypt(self, ciphertext: str, key: int = None) -> str:
        """
        Şifreli metni Caesar Cipher ile çözer.
        
        Args:
            ciphertext: Şifreli metin
            key: Kaydırma miktarı (şifrelemede kullanılan key, varsayılan: 3)
        
        Returns:
            Çözülmüş metin
        """
        if key is None:
            key = self.default_key
        return self.shift_cipher.decrypt(ciphertext, key)

