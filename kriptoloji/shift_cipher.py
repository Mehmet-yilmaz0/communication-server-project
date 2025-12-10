"""
Shift Cipher (Kaydırma Şifresi)
En basit şifreleme yöntemlerinden biri. Her karakteri alfabede belirli bir miktar kaydırır.

Algoritma:
1. Her karakteri alfabetik indekse çevir (A=0, B=1, ..., Z=25)
2. Key değerini ekle (shift)
3. Mod 26 al (alfabede döngü)
4. Yeni indeksi karaktere çevir

Örnek (key=3):
A (0) -> 0+3 = 3 -> D
B (1) -> 1+3 = 4 -> E
Z (25) -> 25+3 = 28 -> 28%26 = 2 -> C
"""

from .utils.text_utils import char_to_index, index_to_char, prepare_text


class ShiftCipher:
    """
    Shift Cipher implementasyonu.
    Her karakteri alfabede key kadar kaydırır.
    """
    
    def encrypt(self, plaintext: str, key: int) -> str:
        """
        Metni şifreler.
        
        Adımlar:
        1. Metni hazırla (büyük harf, sadece alfabetik)
        2. Her karakteri key kadar kaydır
        3. Mod 26 al
        
        Args:
            plaintext: Şifrelenecek metin
            key: Kaydırma miktarı (0-25 arası, negatif olabilir)
        
        Returns:
            Şifreli metin
        """
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        # Key'i mod 26'ya normalize et
        key = key % 26
        
        # Her karakteri kaydır
        ciphertext = []
        for char in text:
            # Karakteri indekse çevir
            index = char_to_index(char)
            # Key ekle ve mod 26 al
            new_index = (index + key) % 26
            # Yeni karakteri al
            ciphertext.append(index_to_char(new_index))
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: int) -> str:
        """
        Şifreli metni çözer.
        
        Adımlar:
        1. Metni hazırla
        2. Her karakteri key kadar geri kaydır (negatif key ekle)
        3. Mod 26 al
        
        Args:
            ciphertext: Şifreli metin
            key: Kaydırma miktarı (şifrelemede kullanılan key)
        
        Returns:
            Çözülmüş metin
        """
        # Decrypt = encrypt ile negatif key
        return self.encrypt(ciphertext, -key)

