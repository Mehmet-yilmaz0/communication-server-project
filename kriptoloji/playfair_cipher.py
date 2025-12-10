"""
Playfair Cipher
5x5 matris kullanarak bigram (iki harf) şifreleme yapar.

Algoritma:
1. Key'den 5x5 matris oluştur (I ve J aynı hücrede)
2. Metni bigram'lara böl (aynı harf yan yana gelirse X ekle)
3. Her bigram için:
   - Aynı satırdaysa: sağdaki karakterleri al (döngüsel)
   - Aynı sütundaysa: alttaki karakterleri al (döngüsel)
   - Değilse: dikdörtgen köşelerini al (satırlar değişir, sütunlar değişir)

Örnek matris (key="MONARCHY"):
M O N A R
C H Y B D
E F G I/J K
L P Q S T
U V W X Z
"""

from .utils.text_utils import prepare_text, remove_duplicates, char_to_index, index_to_char


class PlayfairCipher:
    """
    Playfair Cipher implementasyonu.
    5x5 matris kullanarak bigram şifreleme yapar.
    """
    
    def __init__(self):
        self.alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # J yok (I ile birleşir)
        self.matrix_size = 5
    
    def _create_matrix(self, key: str) -> list:
        """
        Key'den 5x5 Playfair matrisi oluşturur.
        
        Adımlar:
        1. Key'den tekrarları kaldır
        2. Key'i matrise yerleştir
        3. Kalan harfleri alfabetik sırayla ekle (I/J birleşik)
        
        Args:
            key: Matris oluşturmak için key
        
        Returns:
            5x5 matris (liste listesi)
        """
        # Key'i hazırla
        key = prepare_text(key, remove_spaces=True)
        key = key.replace('J', 'I')  # J'yi I'ya çevir
        key = remove_duplicates(key)
        
        # Matrisi oluştur
        matrix = []
        used_chars = set()
        
        # Önce key'i ekle
        for char in key:
            if char not in used_chars:
                used_chars.add(char)
        
        # Key karakterlerini matrise ekle
        key_list = list(key)
        for char in key_list:
            if char not in used_chars:
                continue
            if len(matrix) == 0 or len(matrix[-1]) == 5:
                matrix.append([])
            matrix[-1].append(char)
            used_chars.add(char)
        
        # Kalan harfleri alfabetik sırayla ekle
        for char in self.alphabet:
            if char not in used_chars:
                if len(matrix) == 0 or len(matrix[-1]) == 5:
                    matrix.append([])
                matrix[-1].append(char)
                used_chars.add(char)
        
        return matrix
    
    def _find_position(self, matrix: list, char: str) -> tuple:
        """
        Karakterin matristeki pozisyonunu bulur.
        
        Args:
            matrix: Playfair matrisi
            char: Aranacak karakter
        
        Returns:
            (satır, sütun) tuple'ı
        """
        char = char.upper().replace('J', 'I')
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if cell == char:
                    return (i, j)
        raise ValueError(f"Karakter bulunamadı: {char}")
    
    def _prepare_bigrams(self, text: str) -> list:
        """
        Metni bigram'lara böler.
        
        Kurallar:
        1. Aynı harf yan yana gelirse, aralarına X ekle
        2. Son bigram tek harf kalırsa, X ekle
        
        Args:
            text: Metin
        
        Returns:
            Bigram listesi
        """
        text = prepare_text(text, remove_spaces=True)
        text = text.replace('J', 'I')
        
        bigrams = []
        i = 0
        
        while i < len(text):
            if i + 1 < len(text):
                char1 = text[i]
                char2 = text[i + 1]
                
                # Aynı harf yan yanaysa X ekle
                if char1 == char2:
                    bigrams.append(char1 + 'X')
                    i += 1
                else:
                    bigrams.append(char1 + char2)
                    i += 2
            else:
                # Son karakter tek kalırsa X ekle
                bigrams.append(text[i] + 'X')
                i += 1
        
        return bigrams
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Metni Playfair Cipher ile şifreler.
        
        Args:
            plaintext: Şifrelenecek metin
            key: Matris oluşturmak için key
        
        Returns:
            Şifreli metin
        """
        # Matrisi oluştur
        matrix = self._create_matrix(key)
        
        # Bigram'lara böl
        bigrams = self._prepare_bigrams(plaintext)
        
        # Her bigram'ı şifrele
        ciphertext = []
        for bigram in bigrams:
            char1, char2 = bigram[0], bigram[1]
            row1, col1 = self._find_position(matrix, char1)
            row2, col2 = self._find_position(matrix, char2)
            
            # Aynı satırdaysa: sağdaki karakterleri al
            if row1 == row2:
                new_col1 = (col1 + 1) % 5
                new_col2 = (col2 + 1) % 5
                ciphertext.append(matrix[row1][new_col1] + matrix[row2][new_col2])
            
            # Aynı sütundaysa: alttaki karakterleri al
            elif col1 == col2:
                new_row1 = (row1 + 1) % 5
                new_row2 = (row2 + 1) % 5
                ciphertext.append(matrix[new_row1][col1] + matrix[new_row2][col2])
            
            # Değilse: dikdörtgen köşelerini al
            else:
                ciphertext.append(matrix[row1][col2] + matrix[row2][col1])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Şifreli metni Playfair Cipher ile çözer.
        
        Args:
            ciphertext: Şifreli metin
            key: Şifrelemede kullanılan key
        
        Returns:
            Çözülmüş metin
        """
        # Matrisi oluştur
        matrix = self._create_matrix(key)
        
        # Bigram'lara böl
        bigrams = self._prepare_bigrams(ciphertext)
        
        # Her bigram'ı çöz
        plaintext = []
        for bigram in bigrams:
            char1, char2 = bigram[0], bigram[1]
            row1, col1 = self._find_position(matrix, char1)
            row2, col2 = self._find_position(matrix, char2)
            
            # Aynı satırdaysa: soldaki karakterleri al
            if row1 == row2:
                new_col1 = (col1 - 1) % 5
                new_col2 = (col2 - 1) % 5
                plaintext.append(matrix[row1][new_col1] + matrix[row2][new_col2])
            
            # Aynı sütundaysa: üstteki karakterleri al
            elif col1 == col2:
                new_row1 = (row1 - 1) % 5
                new_row2 = (row2 - 1) % 5
                plaintext.append(matrix[new_row1][col1] + matrix[new_row2][col2])
            
            # Değilse: dikdörtgen köşelerini al
            else:
                plaintext.append(matrix[row1][col2] + matrix[row2][col1])
        
        result = ''.join(plaintext)
        # Son X'i kaldır (padding olabilir)
        if result.endswith('X') and len(result) > 1:
            result = result[:-1]
        
        return result

