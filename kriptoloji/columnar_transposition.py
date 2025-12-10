"""
Columnar Transposition Cipher
Metni sütunlara bölüp sütunları key'e göre sıralayarak şifreler.

Algoritma:
1. Key kelimesinin harflerine göre sütun sırası belirlenir
2. Metni key uzunluğunda satırlara böl
3. Sütunları key'e göre sırala
4. Sütun sütun oku

Örnek (key="ZEBRA"):
Key:        Z E B R A
Sıra:       5 2 1 4 3  (alfabetik sıraya göre: B(1), E(2), R(3), A(4), Z(5))

Plaintext: "HELLO WORLD" (10 karakter, key=5)
Matris:
H E L L O
W O R L D

Sütunlar (key sırasına göre):
3. sütun: L R
1. sütun: H W
4. sütun: L L
2. sütun: E O
5. sütun: O D

Şifreli: LRHWLLEOOD
"""

from .utils.text_utils import prepare_text, pad_text


class ColumnarTransposition:
    """
    Columnar Transposition Cipher implementasyonu.
    Sütunları key'e göre sıralayarak şifreler.
    """
    
    def _get_column_order(self, key: str) -> list:
        """
        Key'den sütun sırasını belirler.
        
        Algoritma:
        1. Key'in her karakterine alfabetik sırada numara ver
        2. Aynı karakterler için sırayla numara ver
        
        Args:
            key: Key kelimesi
        
        Returns:
            Sütun sırası listesi (her eleman sütun numarası)
        """
        # Key'i büyük harfe çevir
        key = key.upper()
        
        # Her karakterin alfabetik sırasını bul
        key_with_indices = []
        for i, char in enumerate(key):
            key_with_indices.append((char, i))
        
        # Alfabetik sıraya göre sırala
        sorted_key = sorted(key_with_indices, key=lambda x: (x[0], x[1]))
        
        # Sütun sırasını oluştur
        column_order = [0] * len(key)
        for new_order, (char, original_index) in enumerate(sorted_key):
            column_order[original_index] = new_order
        
        return column_order
    
    def _get_inverse_order(self, column_order: list) -> list:
        """
        Sütun sırasının tersini hesaplar.
        
        Args:
            column_order: Sütun sırası
        
        Returns:
            Ters sütun sırası
        """
        inverse = [0] * len(column_order)
        for i, order in enumerate(column_order):
            inverse[order] = i
        return inverse
    
    def encrypt(self, plaintext: str, key: str) -> str:
        """
        Metni Columnar Transposition ile şifreler.
        
        Adımlar:
        1. Metni key uzunluğunda satırlara böl
        2. Sütun sırasını belirle
        3. Sütunları sıraya göre oku
        
        Args:
            plaintext: Şifrelenecek metin
            key: Key kelimesi
        
        Returns:
            Şifreli metin
        """
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        if len(key) == 0:
            raise ValueError("Key boş olamaz")
        
        key = key.upper()
        key_len = len(key)
        
        # Metni key uzunluğuna kadar doldur
        padded_text = pad_text(text, ((len(text) + key_len - 1) // key_len) * key_len, 'X')
        
        # Sütun sırasını belirle
        column_order = self._get_column_order(key)
        
        # Matrisi oluştur (satırlar)
        num_rows = len(padded_text) // key_len
        matrix = []
        text_index = 0
        
        for i in range(num_rows):
            row = []
            for j in range(key_len):
                row.append(padded_text[text_index])
                text_index += 1
            matrix.append(row)
        
        # Sütunları sıraya göre oku
        ciphertext = []
        sorted_columns = sorted(range(key_len), key=lambda x: column_order[x])
        
        for col_idx in sorted_columns:
            for row in matrix:
                ciphertext.append(row[col_idx])
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: str) -> str:
        """
        Şifreli metni Columnar Transposition ile çözer.
        
        Adımlar:
        1. Sütun sırasını belirle
        2. Şifreli metni sütunlara yerleştir (ters sırayla)
        3. Satır satır oku
        
        Args:
            ciphertext: Şifreli metin
            key: Şifrelemede kullanılan key
        
        Returns:
            Çözülmüş metin
        """
        # Metni hazırla
        text = prepare_text(ciphertext, remove_spaces=True)
        
        if len(key) == 0:
            raise ValueError("Key boş olamaz")
        
        key = key.upper()
        key_len = len(key)
        
        # Sütun sırasını belirle
        column_order = self._get_column_order(key)
        
        # Toplam karakter sayısı
        total_chars = len(text)
        num_rows = (total_chars + key_len - 1) // key_len
        
        # Sütun sırasına göre sıralı sütun indeksleri
        sorted_columns = sorted(range(key_len), key=lambda x: column_order[x])
        
        # Her sütunda kaç karakter var
        chars_per_col = total_chars // key_len
        extra_chars = total_chars % key_len
        
        # Şifreli metni sütunlara yerleştir
        text_index = 0
        columns = [[] for _ in range(key_len)]
        
        for col_order_idx, col_idx in enumerate(sorted_columns):
            # Bu sütuna kaç karakter gelecek
            if col_order_idx < extra_chars:
                col_size = chars_per_col + 1
            else:
                col_size = chars_per_col
            
            # Bu sütuna karakterleri yerleştir
            for _ in range(col_size):
                if text_index < len(text):
                    columns[col_idx].append(text[text_index])
                    text_index += 1
        
        # Matrisi oluştur (sütunlardan satırlara)
        matrix = []
        for row_idx in range(num_rows):
            row = []
            for col_idx in range(key_len):
                if row_idx < len(columns[col_idx]):
                    row.append(columns[col_idx][row_idx])
                else:
                    row.append('X')  # Padding
            matrix.append(row)
        
        # Satır satır oku
        plaintext = []
        for row in matrix:
            plaintext.extend(row)
        
        result = ''.join(plaintext)
        # Son X'leri kaldır (padding)
        result = result.rstrip('X')
        
        return result

