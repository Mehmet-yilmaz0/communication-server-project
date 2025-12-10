"""
Substitution Cipher (Yerine Koyma Şifresi)
Her karakteri başka bir karakterle değiştirir.

Algoritma:
1. Key olarak bir permütasyon tablosu kullanılır (26 harf için)
2. Her karakteri key tablosundaki karşılığıyla değiştir
3. Decrypt için ters tablo kullanılır

Örnek key (alfabetik sıra):
A -> Z, B -> Y, C -> X, ..., Z -> A (ters alfabe)

Örnek key (rastgele):
A -> M, B -> N, C -> B, D -> V, ..., Z -> Q
"""

from .utils.text_utils import char_to_index, index_to_char, prepare_text


class SubstitutionCipher:
    """
    Substitution Cipher implementasyonu.
    Key olarak 26 karakterlik bir permütasyon string'i kullanır.
    """
    
    def __init__(self):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    def _validate_key(self, key: str) -> str:
        """
        Key'i doğrular ve normalize eder.
        
        Args:
            key: 26 karakterlik permütasyon string'i
        
        Returns:
            Normalize edilmiş key
        """
        # Büyük harfe çevir ve sadece alfabetik karakterleri al
        key = ''.join(c for c in key.upper() if c.isalpha())
        
        # Key uzunluğu kontrolü
        if len(key) < 26:
            raise ValueError("Key en az 26 karakter olmalı")
        
        # İlk 26 karakteri al
        key = key[:26]
        
        # Her harfin key'de bir kez geçtiğini kontrol et
        seen = set()
        for char in key:
            if char in seen:
                raise ValueError(f"Key'de tekrarlanan karakter: {char}")
            seen.add(char)
        
        return key
    
    def _create_decrypt_key(self, encrypt_key: str) -> str:
        """
        Şifreleme key'inden çözme key'ini oluşturur.
        
        Algoritma:
        - Encrypt key: A -> key[0], B -> key[1], ...
        - Decrypt key: key[0] -> A, key[1] -> B, ...
        
        Args:
            encrypt_key: Şifreleme key'i
        
        Returns:
            Çözme key'i
        """
        decrypt_key = [''] * 26
        for i, char in enumerate(encrypt_key):
            # key[i] karakteri, orijinal alfabedeki i. karaktere karşılık gelir
            original_index = char_to_index(char)
            decrypt_key[original_index] = index_to_char(i)
        
        return ''.join(decrypt_key)
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Metni Substitution Cipher ile şifreler.
        
        Adımlar:
        1. Key'i doğrula
        2. Her karakteri key tablosundaki karşılığıyla değiştir
        
        Args:
            plaintext: Şifrelenecek metin
            key: 26 karakterlik permütasyon string'i (A-Z için mapping)
        
        Returns:
            Şifreli metin
        """
        # Key'i doğrula
        key = self._validate_key(key)
        
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        # Her karakteri key'e göre değiştir
        ciphertext = []
        for char in text:
            # Karakterin alfabedeki indeksini bul
            index = char_to_index(char)
            # Key'deki karşılığını al
            ciphertext.append(key[index])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Şifreli metni Substitution Cipher ile çözer.
        
        Adımlar:
        1. Key'i doğrula
        2. Decrypt key'ini oluştur
        3. Her karakteri decrypt key'e göre değiştir
        
        Args:
            ciphertext: Şifreli metin
            key: Şifrelemede kullanılan key
        
        Returns:
            Çözülmüş metin
        """
        # Key'i doğrula
        key = self._validate_key(key)
        
        # Decrypt key'ini oluştur
        decrypt_key = self._create_decrypt_key(key)
        
        # Metni hazırla
        text = prepare_text(ciphertext, remove_spaces=True)
        
        # Her karakteri decrypt key'e göre değiştir
        plaintext = []
        for char in text:
            # Karakterin alfabedeki indeksini bul
            index = char_to_index(char)
            # Decrypt key'deki karşılığını al
            plaintext.append(decrypt_key[index])
        
        return ''.join(plaintext)

