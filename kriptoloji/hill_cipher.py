"""
Hill Cipher
Matris tabanlı şifreleme. Her karakter grubu bir matrisle çarpılır.

Algoritma:
1. NxN anahtar matrisi seç (2x2 veya 3x3)
2. Metni N'li gruplara böl
3. Her grubu vektör olarak temsil et
4. Vektörü anahtar matrisiyle çarp (mod 26)
5. Sonuç vektörü karakterlere çevir

Örnek (2x2 matris, key=[[3,3],[2,5]]):
Plaintext: "HELLO" -> "HE", "LL", "OX" (padding)
HE -> [7, 4]
[7, 4] * [[3,3],[2,5]] = [7*3+4*2, 7*3+4*5] = [29, 41]
Mod 26: [3, 15] -> "DP"
"""

from .utils.matrix_utils import (
    create_matrix, matrix_multiply, text_to_matrix, 
    matrix_to_text, matrix_inverse
)
from .utils.text_utils import prepare_text, pad_text


class HillCipher:
    """
    Hill Cipher implementasyonu.
    Matris çarpımı kullanarak şifreleme yapar.
    """
    
    def __init__(self):
        self.supported_sizes = [2, 3]  # 2x2 ve 3x3 matrisler
    
    def _validate_key_matrix(self, key_matrix: list) -> list:
        """
        Anahtar matrisini doğrular ve normalize eder.
        
        Args:
            key_matrix: Anahtar matrisi (2x2 veya 3x3)
        
        Returns:
            Doğrulanmış matris
        """
        n = len(key_matrix)
        
        if n not in self.supported_sizes:
            raise ValueError(f"Matris boyutu {n}x{n} desteklenmiyor. Sadece 2x2 ve 3x3 destekleniyor.")
        
        # Her satırın uzunluğunu kontrol et
        for i, row in enumerate(key_matrix):
            if len(row) != n:
                raise ValueError(f"Matris kare değil: satır {i} uzunluğu {len(row)}, beklenen {n}")
        
        # Mod 26'ya normalize et
        normalized = create_matrix(n, n, 0)
        for i in range(n):
            for j in range(n):
                normalized[i][j] = key_matrix[i][j] % 26
        
        return normalized
    
    def encrypt(self, plaintext: str, key_matrix: list) -> str:
        """
        Metni Hill Cipher ile şifreler.
        
        Adımlar:
        1. Anahtar matrisini doğrula
        2. Metni N'li gruplara böl (N = matris boyutu)
        3. Her grubu matrisle çarp
        4. Sonuçları birleştir
        
        Args:
            plaintext: Şifrelenecek metin
            key_matrix: Anahtar matrisi (2x2 veya 3x3 liste listesi)
        
        Returns:
            Şifreli metin
        """
        # Anahtar matrisini doğrula
        key = self._validate_key_matrix(key_matrix)
        n = len(key)
        
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        # Metni N'li gruplara böl ve padding ekle
        if len(text) % n != 0:
            text = pad_text(text, ((len(text) + n - 1) // n) * n, 'X')
        
        # Grupları şifrele
        ciphertext_blocks = []
        
        for i in range(0, len(text), n):
            # Grubu al
            block = text[i:i + n]
            
            # Vektörü oluştur (1xN matris)
            vector = text_to_matrix(block, 1, n)
            
            # Matris çarpımı: vector * key (1xN * NxN = 1xN)
            # Not: text_to_matrix Nx1 döndürür, bu yüzden transpoze etmemiz gerekebilir
            # Basit yaklaşım: vektörü Nx1 olarak oluştur, sonra key ile çarp
            
            # Vektörü Nx1 matris olarak oluştur
            vector_matrix = [[0] for _ in range(n)]
            for j, char in enumerate(block):
                from .utils.text_utils import char_to_index
                vector_matrix[j][0] = char_to_index(char)
            
            # Key * vector (NxN * Nx1 = Nx1)
            result_matrix = matrix_multiply(key, vector_matrix)
            
            # Sonucu metne çevir
            result_text = matrix_to_text(result_matrix)
            ciphertext_blocks.append(result_text)
        
        return ''.join(ciphertext_blocks)
    
    def decrypt(self, ciphertext: str, key_matrix: list) -> str:
        """
        Şifreli metni Hill Cipher ile çözer.
        
        Adımlar:
        1. Anahtar matrisini doğrula
        2. Ters matrisi hesapla (mod 26)
        3. Metni N'li gruplara böl
        4. Her grubu ters matrisle çarp
        5. Sonuçları birleştir
        
        Args:
            ciphertext: Şifreli metin
            key_matrix: Şifrelemede kullanılan anahtar matrisi
        
        Returns:
            Çözülmüş metin
        """
        # Anahtar matrisini doğrula
        key = self._validate_key_matrix(key_matrix)
        n = len(key)
        
        # Ters matrisi hesapla
        try:
            inverse_key = matrix_inverse(key)
        except ValueError as e:
            raise ValueError(f"Anahtar matrisinin modüler tersi yok: {e}")
        
        # Metni hazırla
        text = prepare_text(ciphertext, remove_spaces=True)
        
        if len(text) % n != 0:
            raise ValueError(f"Şifreli metin uzunluğu {n}'in katı olmalı")
        
        # Grupları çöz
        plaintext_blocks = []
        
        for i in range(0, len(text), n):
            # Grubu al
            block = text[i:i + n]
            
            # Vektörü Nx1 matris olarak oluştur
            vector_matrix = [[0] for _ in range(n)]
            for j, char in enumerate(block):
                from .utils.text_utils import char_to_index
                vector_matrix[j][0] = char_to_index(char)
            
            # Inverse key * vector (NxN * Nx1 = Nx1)
            result_matrix = matrix_multiply(inverse_key, vector_matrix)
            
            # Sonucu metne çevir
            result_text = matrix_to_text(result_matrix)
            plaintext_blocks.append(result_text)
        
        result = ''.join(plaintext_blocks)
        # Son X'leri kaldır (padding)
        result = result.rstrip('X')
        
        return result

