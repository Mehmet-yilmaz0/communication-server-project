"""
Polybius Square Cipher
5x5 matris kullanarak her karakteri iki rakamla temsil eder.

Algoritma:
1. 5x5 matris oluştur (I ve J aynı hücrede, genelde I kullanılır)
2. Her karakteri (satır, sütun) koordinatlarıyla temsil et
3. Şifreleme: Karakter -> (satır+1, sütun+1) -> "satırsütun"
4. Çözme: "satırsütun" -> (satır-1, sütun-1) -> Karakter

Örnek matris (key="POLYBIUS"):
   1 2 3 4 5
1  P O L Y B
2  I U S A C
3  D E F G H
4  J K M N Q
5  R T V W X
6  Z (5x6 veya standart 5x5)

Standart matris (key yok):
   1 2 3 4 5
1  A B C D E
2  F G H I/J K
3  L M N O P
4  Q R S T U
5  V W X Y Z
"""

from .utils.text_utils import prepare_text, remove_duplicates


class PolybiusCipher:
    """
    Polybius Square Cipher implementasyonu.
    5x5 matris kullanarak karakterleri koordinatlara çevirir.
    """
    
    def __init__(self):
        self.matrix_size = 5
        self.standard_alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # J yok (I ile birleşir)
    
    def _create_matrix(self, key: str = None) -> list:
        """
        Polybius matrisi oluşturur.
        
        Args:
            key: Key kelimesi (varsayılan: None, standart matris)
        
        Returns:
            5x5 matris
        """
        if key is None:
            # Standart matris
            matrix = []
            alphabet = self.standard_alphabet
            for i in range(self.matrix_size):
                row = []
                for j in range(self.matrix_size):
                    idx = i * self.matrix_size + j
                    if idx < len(alphabet):
                        row.append(alphabet[idx])
                matrix.append(row)
            return matrix
        
        # Key'den matris oluştur
        key = prepare_text(key, remove_spaces=True)
        key = key.replace('J', 'I')
        key = remove_duplicates(key)
        
        # Kullanılan karakterleri takip et
        used_chars = set(key)
        matrix = []
        
        # Önce key'i ekle
        key_list = list(key)
        for char in key_list:
            if len(matrix) == 0 or len(matrix[-1]) == self.matrix_size:
                matrix.append([])
            if char not in used_chars:
                continue
            matrix[-1].append(char)
            used_chars.add(char)
        
        # Kalan harfleri ekle
        for char in self.standard_alphabet:
            if char not in used_chars:
                if len(matrix) == 0 or len(matrix[-1]) == self.matrix_size:
                    matrix.append([])
                matrix[-1].append(char)
                used_chars.add(char)
        
        return matrix
    
    def _find_position(self, matrix: list, char: str) -> tuple:
        """
        Karakterin matristeki pozisyonunu bulur.
        
        Args:
            matrix: Polybius matrisi
            char: Aranacak karakter
        
        Returns:
            (satır, sütun) tuple'ı (0-indexed)
        """
        char = char.upper().replace('J', 'I')
        for i, row in enumerate(matrix):
            for j, cell in enumerate(row):
                if cell == char:
                    return (i, j)
        raise ValueError(f"Karakter bulunamadı: {char}")
    
    def encrypt(self, plaintext: str, key: str = None) -> str:
        """
        Metni Polybius Cipher ile şifreler.
        
        Adımlar:
        1. Matrisi oluştur
        2. Her karakteri (satır+1, sütun+1) formatına çevir
        3. Koordinatları birleştir
        
        Args:
            plaintext: Şifrelenecek metin
            key: Key kelimesi (varsayılan: None, standart matris)
        
        Returns:
            Şifreli metin (rakamlar: "11223344" gibi)
        """
        # Matrisi oluştur
        matrix = self._create_matrix(key)
        
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        text = text.replace('J', 'I')
        
        # Her karakteri koordinatlara çevir
        ciphertext = []
        for char in text:
            row, col = self._find_position(matrix, char)
            # 1-indexed koordinatlar (1-5 arası)
            ciphertext.append(str(row + 1))
            ciphertext.append(str(col + 1))
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: str = None) -> str:
        """
        Şifreli metni Polybius Cipher ile çözer.
        
        Adımlar:
        1. Matrisi oluştur
        2. Şifreli metni ikişer rakam olarak oku
        3. Her (satır, sütun) çiftini karaktere çevir
        
        Args:
            ciphertext: Şifreli metin (rakamlar: "11223344" gibi)
            key: Şifrelemede kullanılan key
        
        Returns:
            Çözülmüş metin
        """
        # Matrisi oluştur
        matrix = self._create_matrix(key)
        
        # Sadece rakamları al
        digits = ''.join(c for c in ciphertext if c.isdigit())
        
        if len(digits) % 2 != 0:
            raise ValueError("Şifreli metin çift sayıda rakam içermeli")
        
        # İkişer rakam oku
        plaintext = []
        for i in range(0, len(digits), 2):
            row_str = digits[i]
            col_str = digits[i + 1]
            
            # 1-indexed'den 0-indexed'e çevir
            row = int(row_str) - 1
            col = int(col_str) - 1
            
            # Geçerlilik kontrolü
            if not (0 <= row < self.matrix_size and 0 <= col < self.matrix_size):
                raise ValueError(f"Geçersiz koordinat: ({row_str}, {col_str})")
            
            # Karakteri al
            plaintext.append(matrix[row][col])
        
        return ''.join(plaintext)

