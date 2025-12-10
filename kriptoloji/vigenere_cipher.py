"""
Vigenère Cipher
Çoklu alfabetik şifreleme yöntemi. Key kelimesi tekrarlanarak kullanılır.

Algoritma:
1. Key kelimesini metin uzunluğuna kadar tekrarla
2. Her karakter için:
   - Plaintext karakteri: P[i]
   - Key karakteri: K[i]
   - Ciphertext: (P[i] + K[i]) mod 26

Örnek (key="KEY"):
Plaintext:  H E L L O
Key:        K E Y K E
Ciphertext: R I B D S

H(7) + K(10) = 17 -> R
E(4) + E(4) = 8 -> I
L(11) + Y(24) = 35 mod 26 = 9 -> J (ama bu örnekte farklı olabilir)
"""

from .utils.text_utils import prepare_text, char_to_index, index_to_char


class VigenereCipher:
    """
    Vigenère Cipher implementasyonu.
    Key kelimesini tekrarlayarak her karakteri ayrı shift ile şifreler.
    """
    
    def _prepare_key(self, key: str, length: int) -> str:
        """
        Key'i metin uzunluğuna kadar tekrarlar.
        
        Args:
            key: Key kelimesi
            length: Hedef uzunluk
        
        Returns:
            Tekrarlanmış key
        """
        key = prepare_text(key, remove_spaces=True)
        if len(key) == 0:
            raise ValueError("Key boş olamaz")
        
        # Key'i uzunluğa kadar tekrarla
        repeated_key = (key * ((length // len(key)) + 1))[:length]
        return repeated_key
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Metni Vigenère Cipher ile şifreler.
        
        Adımlar:
        1. Metni hazırla
        2. Key'i metin uzunluğuna kadar tekrarla
        3. Her karakter için: (plaintext[i] + key[i]) mod 26
        
        Args:
            plaintext: Şifrelenecek metin
            key: Key kelimesi
        
        Returns:
            Şifreli metin
        """
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        # Key'i hazırla
        key_text = self._prepare_key(key, len(text))
        
        # Her karakteri şifrele
        ciphertext = []
        for i in range(len(text)):
            # Karakterleri indekse çevir
            p_index = char_to_index(text[i])
            k_index = char_to_index(key_text[i])
            
            # Topla ve mod 26 al
            c_index = (p_index + k_index) % 26
            
            # Yeni karakteri al
            ciphertext.append(index_to_char(c_index))
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Şifreli metni Vigenère Cipher ile çözer.
        
        Adımlar:
        1. Metni hazırla
        2. Key'i metin uzunluğuna kadar tekrarla
        3. Her karakter için: (ciphertext[i] - key[i]) mod 26
        
        Args:
            ciphertext: Şifreli metin
            key: Şifrelemede kullanılan key
        
        Returns:
            Çözülmüş metin
        """
        # Metni hazırla
        text = prepare_text(ciphertext, remove_spaces=True)
        
        # Key'i hazırla
        key_text = self._prepare_key(key, len(text))
        
        # Her karakteri çöz
        plaintext = []
        for i in range(len(text)):
            # Karakterleri indekse çevir
            c_index = char_to_index(text[i])
            k_index = char_to_index(key_text[i])
            
            # Çıkar ve mod 26 al
            p_index = (c_index - k_index) % 26
            if p_index < 0:
                p_index += 26
            
            # Yeni karakteri al
            plaintext.append(index_to_char(p_index))
        
        return ''.join(plaintext)

