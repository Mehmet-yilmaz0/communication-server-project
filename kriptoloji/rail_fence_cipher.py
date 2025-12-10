"""
Rail Fence Cipher (Zigzag Şifresi)
Metni zigzag şeklinde yazarak şifreler.

Algoritma:
1. Metni N satırlı zigzag şeklinde yaz
2. Şifreleme: Her satırı sırayla oku
3. Çözme: Şifreli metni zigzag şeklinde yerleştir, sonra satır satır oku

Örnek (rails=3, plaintext="HELLO WORLD"):
H . . . O . . . R . . .
E . L . L . O . . . L . D
L . . . W . . . . . . .

Şifreli: HORELOLWD (satır satır okunur)
"""

from .utils.text_utils import prepare_text


class RailFenceCipher:
    """
    Rail Fence Cipher implementasyonu.
    Metni zigzag şeklinde yazarak şifreler.
    """
    
    def encrypt(self, plaintext: str, rails: int) -> str:
        """
        Metni Rail Fence Cipher ile şifreler.
        
        Adımlar:
        1. Metni hazırla
        2. N satırlı zigzag matrisi oluştur
        3. Metni zigzag şeklinde yerleştir
        4. Her satırı sırayla oku
        
        Args:
            plaintext: Şifrelenecek metin
            rails: Ray sayısı (satır sayısı, en az 2)
        
        Returns:
            Şifreli metin
        """
        if rails < 2:
            raise ValueError("Rails en az 2 olmalı")
        
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        if len(text) == 0:
            return ""
        
        # Zigzag matrisi oluştur (her satır bir liste)
        matrix = [[] for _ in range(rails)]
        
        # Zigzag yerleştirme
        row = 0
        direction = 1  # 1: aşağı, -1: yukarı
        
        for char in text:
            # Karakteri mevcut satıra ekle
            matrix[row].append(char)
            
            # Bir sonraki satırı belirle
            row += direction
            
            # Yön değiştir (üst veya alt sınıra ulaşıldığında)
            if row == 0:
                direction = 1
            elif row == rails - 1:
                direction = -1
        
        # Her satırı sırayla oku
        ciphertext = []
        for row_list in matrix:
            ciphertext.extend(row_list)
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, rails: int) -> str:
        """
        Şifreli metni Rail Fence Cipher ile çözer.
        
        Adımlar:
        1. Metni hazırla
        2. Zigzag pattern'i hesapla (hangi pozisyonlar hangi satırda)
        3. Şifreli metni zigzag şeklinde yerleştir
        4. Zigzag şeklinde oku
        
        Args:
            ciphertext: Şifreli metin
            rails: Ray sayısı (şifrelemede kullanılan rails)
        
        Returns:
            Çözülmüş metin
        """
        if rails < 2:
            raise ValueError("Rails en az 2 olmalı")
        
        # Metni hazırla
        text = prepare_text(ciphertext, remove_spaces=True)
        
        if len(text) == 0:
            return ""
        
        # Zigzag pattern'i oluştur (her pozisyonun hangi satırda olduğunu göster)
        pattern = []
        row = 0
        direction = 1
        
        for _ in range(len(text)):
            pattern.append(row)
            row += direction
            if row == 0:
                direction = 1
            elif row == rails - 1:
                direction = -1
        
        # Her satırda kaç karakter olduğunu say
        row_counts = [0] * rails
        for row_num in pattern:
            row_counts[row_num] += 1
        
        # Şifreli metni satırlara böl
        matrix = [[] for _ in range(rails)]
        text_index = 0
        
        for row_num in range(rails):
            # Bu satıra ait karakterleri al
            count = row_counts[row_num]
            matrix[row_num] = list(text[text_index:text_index + count])
            text_index += count
        
        # Zigzag şeklinde oku
        plaintext = []
        row_indices = [0] * rails  # Her satırda okuma indeksi
        
        for pos in range(len(text)):
            # Bu pozisyondaki satırı bul
            target_row = pattern[pos]
            
            # Bu satırdan karakteri al
            char = matrix[target_row][row_indices[target_row]]
            plaintext.append(char)
            row_indices[target_row] += 1
        
        return ''.join(plaintext)

