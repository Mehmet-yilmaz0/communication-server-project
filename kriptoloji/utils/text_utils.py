"""
Metin İşleme Yardımcı Fonksiyonları
Kriptografi algoritmaları için ortak metin işleme fonksiyonları.
"""


def prepare_text(text: str, remove_spaces: bool = False, remove_punctuation: bool = True) -> str:
    """
    Metni şifreleme için hazırlar.
    
    Adımlar:
    1. Tüm karakterleri büyük harfe çevir
    2. İsteğe bağlı olarak boşlukları kaldır
    3. İsteğe bağlı olarak noktalama işaretlerini kaldır
    4. Sadece alfabetik karakterleri tut
    
    Args:
        text: İşlenecek metin
        remove_spaces: Boşlukları kaldır (varsayılan: False)
        remove_punctuation: Noktalama işaretlerini kaldır (varsayılan: True)
    
    Returns:
        Hazırlanmış metin
    """
    # Büyük harfe çevir
    text = text.upper()
    
    # Sadece alfabetik karakterleri ve boşlukları tut
    result = []
    for char in text:
        if char.isalpha():
            result.append(char)
        elif char == ' ' and not remove_spaces:
            result.append(char)
        # Noktalama işaretleri ve diğer karakterler atlanır
    
    return ''.join(result)


def split_into_blocks(text: str, block_size: int) -> list:
    """
    Metni belirtilen boyutta bloklara böler.
    
    Args:
        text: Bölünecek metin
        block_size: Blok boyutu
    
    Returns:
        Blokların listesi
    """
    blocks = []
    for i in range(0, len(text), block_size):
        block = text[i:i + block_size]
        # Son bloğu doldur (gerekirse)
        if len(block) < block_size:
            block += 'X' * (block_size - len(block))
        blocks.append(block)
    return blocks


def remove_duplicates(text: str) -> str:
    """
    Metindeki tekrarlanan karakterleri kaldırır (sırayı koruyarak).
    
    Args:
        text: İşlenecek metin
    
    Returns:
        Tekrarları kaldırılmış metin
    """
    seen = set()
    result = []
    for char in text:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return ''.join(result)


def char_to_index(char: str) -> int:
    """
    Karakteri alfabetik indekse çevirir (A=0, B=1, ..., Z=25).
    
    Args:
        char: Karakter (tek karakter, büyük harf olmalı)
    
    Returns:
        Alfabetik indeks (0-25)
    """
    if not char.isalpha():
        raise ValueError(f"Geçersiz karakter: {char}")
    return ord(char.upper()) - ord('A')


def index_to_char(index: int) -> str:
    """
    Alfabetik indeksi karaktere çevirir (0=A, 1=B, ..., 25=Z).
    
    Args:
        index: Alfabetik indeks (0-25)
    
    Returns:
        Karakter (büyük harf)
    """
    if not (0 <= index <= 25):
        raise ValueError(f"Geçersiz indeks: {index}")
    return chr(index + ord('A'))


def pad_text(text: str, length: int, pad_char: str = 'X') -> str:
    """
    Metni belirtilen uzunluğa kadar doldurur.
    
    Args:
        text: Doldurulacak metin
        length: Hedef uzunluk
        pad_char: Doldurma karakteri (varsayılan: 'X')
    
    Returns:
        Doldurulmuş metin
    """
    if len(text) >= length:
        return text[:length]
    return text + pad_char * (length - len(text))

