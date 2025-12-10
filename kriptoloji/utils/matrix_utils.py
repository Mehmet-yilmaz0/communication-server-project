"""
Matris İşleme Yardımcı Fonksiyonları
Hill Cipher ve diğer matris tabanlı algoritmalar için matris işlemleri.
"""


def create_matrix(rows: int, cols: int, fill_value=0):
    """
    Belirtilen boyutlarda matris oluşturur.
    
    Args:
        rows: Satır sayısı
        cols: Sütun sayısı
        fill_value: Doldurma değeri (varsayılan: 0)
    
    Returns:
        Matris (2D liste)
    """
    return [[fill_value for _ in range(cols)] for _ in range(rows)]


def matrix_multiply(A, B):
    """
    İki matrisi çarpar (A * B).
    
    Algoritma:
    1. A'nın sütun sayısı B'nin satır sayısına eşit olmalı
    2. Sonuç matrisi: A'nın satır sayısı x B'nin sütun sayısı
    3. Her eleman: A[i][k] * B[k][j] toplamı
    
    Args:
        A: İlk matris
        B: İkinci matris
    
    Returns:
        Çarpım matrisi
    """
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])
    
    if cols_A != rows_B:
        raise ValueError("Matris boyutları uyumsuz: A'nın sütun sayısı B'nin satır sayısına eşit olmalı")
    
    # Sonuç matrisini oluştur
    result = create_matrix(rows_A, cols_B, 0)
    
    # Matris çarpımı
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]
    
    return result


def matrix_determinant(matrix):
    """
    Matrisin determinantını hesaplar (sadece 2x2 ve 3x3 için).
    
    2x2 matris için:
    det = a*d - b*c
    
    3x3 matris için (Sarrus kuralı):
    det = a(ei-fh) - b(di-fg) + c(dh-eg)
    
    Args:
        matrix: Kare matris (2x2 veya 3x3)
    
    Returns:
        Determinant değeri
    """
    n = len(matrix)
    
    if n != len(matrix[0]):
        raise ValueError("Matris kare olmalı")
    
    if n == 2:
        # 2x2 determinant
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    elif n == 3:
        # 3x3 determinant (Sarrus kuralı)
        a, b, c = matrix[0][0], matrix[0][1], matrix[0][2]
        d, e, f = matrix[1][0], matrix[1][1], matrix[1][2]
        g, h, i = matrix[2][0], matrix[2][1], matrix[2][2]
        
        det = (a * (e * i - f * h) - 
               b * (d * i - f * g) + 
               c * (d * h - e * g))
        return det
    
    else:
        raise ValueError("Sadece 2x2 ve 3x3 matrisler destekleniyor")


def matrix_inverse(matrix):
    """
    Matrisin modüler tersini hesaplar (mod 26).
    
    Algoritma:
    1. Determinantı hesapla
    2. Determinantın mod 26'da tersini bul
    3. Adjoint matrisi hesapla
    4. Adjoint * det_inverse (mod 26)
    
    Args:
        matrix: Kare matris (2x2 veya 3x3)
    
    Returns:
        Ters matris (mod 26)
    """
    n = len(matrix)
    
    if n == 2:
        # 2x2 matris tersi
        det = matrix_determinant(matrix)
        det_mod = mod_inverse(det, 26)
        
        if det_mod is None:
            raise ValueError("Matrisin modüler tersi yok (determinant mod 26'da tersinir değil)")
        
        # Adjoint matris (2x2 için)
        adjoint = [
            [matrix[1][1], -matrix[0][1]],
            [-matrix[1][0], matrix[0][0]]
        ]
        
        # Ters matris = adjoint * det_inverse (mod 26)
        inverse = create_matrix(2, 2, 0)
        for i in range(2):
            for j in range(2):
                inverse[i][j] = (adjoint[i][j] * det_mod) % 26
                if inverse[i][j] < 0:
                    inverse[i][j] += 26
        
        return inverse
    
    elif n == 3:
        # 3x3 matris tersi
        det = matrix_determinant(matrix)
        det_mod = mod_inverse(det, 26)
        
        if det_mod is None:
            raise ValueError("Matrisin modüler tersi yok")
        
        # Cofactor matrisi hesapla
        cofactor = create_matrix(3, 3, 0)
        for i in range(3):
            for j in range(3):
                # Minor matrisi oluştur
                minor = []
                for row in range(3):
                    if row != i:
                        minor_row = []
                        for col in range(3):
                            if col != j:
                                minor_row.append(matrix[row][col])
                        minor.append(minor_row)
                
                # Cofactor = (-1)^(i+j) * minor_determinant
                sign = 1 if (i + j) % 2 == 0 else -1
                minor_det = matrix_determinant(minor)
                cofactor[i][j] = sign * minor_det
        
        # Adjoint = cofactor'un transpozu
        adjoint = [[cofactor[j][i] for j in range(3)] for i in range(3)]
        
        # Ters matris = adjoint * det_inverse (mod 26)
        inverse = create_matrix(3, 3, 0)
        for i in range(3):
            for j in range(3):
                inverse[i][j] = (adjoint[i][j] * det_mod) % 26
                if inverse[i][j] < 0:
                    inverse[i][j] += 26
        
        return inverse
    
    else:
        raise ValueError("Sadece 2x2 ve 3x3 matrisler destekleniyor")


def mod_inverse(a: int, m: int):
    """
    Modüler ters hesaplar (Extended Euclidean Algorithm).
    
    Algoritma:
    ax ≡ 1 (mod m) denklemini çözer.
    Extended Euclidean Algorithm kullanarak gcd(a, m) = 1 ise tersi bulur.
    
    Args:
        a: Tersinir sayı
        m: Mod değeri
    
    Returns:
        Modüler ters (veya None eğer yoksa)
    """
    # Extended Euclidean Algorithm
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % m, m)
    
    if gcd != 1:
        return None  # Tersinir değil
    
    return (x % m + m) % m


def text_to_matrix(text: str, rows: int, cols: int):
    """
    Metni matrise çevirir (her karakter alfabetik indekse çevrilir).
    
    Args:
        text: Metin
        rows: Matris satır sayısı
        cols: Matris sütun sayısı
    
    Returns:
        Matris (her eleman 0-25 arası)
    """
    from .text_utils import char_to_index
    
    matrix = create_matrix(rows, cols, 0)
    text_index = 0
    
    for i in range(rows):
        for j in range(cols):
            if text_index < len(text):
                matrix[i][j] = char_to_index(text[text_index])
                text_index += 1
            else:
                matrix[i][j] = char_to_index('X')  # Padding
    
    return matrix


def matrix_to_text(matrix):
    """
    Matrisi metne çevirir.
    
    Args:
        matrix: Matris (her eleman 0-25 arası)
    
    Returns:
        Metin
    """
    from .text_utils import index_to_char
    
    text = []
    for row in matrix:
        for val in row:
            text.append(index_to_char(val % 26))
    
    return ''.join(text)

