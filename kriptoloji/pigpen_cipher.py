"""
Pigpen Cipher (Masonic Cipher)
Görsel şablon tabanlı şifreleme. Her karakter özel bir şekille temsil edilir.

Algoritma:
1. Her karakter için önceden tanımlı şablon kullan
2. Şifreleme: Karakter -> Şablon sembolü
3. Çözme: Şablon sembolü -> Karakter

Pigpen şablonları:
- A, B, C, D: Kare içinde nokta (farklı köşeler)
- E, F, G, H: X içinde nokta (farklı köşeler)
- I, J, K, L: Kare (boş, farklı köşeler)
- M, N, O, P: X (boş, farklı köşeler)
- Q, R, S, T: Kare içinde çizgi (farklı yönler)
- U, V, W, X: X içinde çizgi (farklı yönler)
- Y, Z: Özel semboller

Bu implementasyonda sembolleri karakter kodlarıyla temsil ediyoruz.
"""

from .utils.text_utils import prepare_text


class PigpenCipher:
    """
    Pigpen Cipher implementasyonu.
    Görsel şablonları karakter kodlarıyla temsil eder.
    """
    
    def __init__(self):
        # Pigpen şablon haritası
        # Her karakter için özel bir kod (2 karakterlik)
        # Format: [şekil_tipi][pozisyon]
        # Şekil tipleri: S (square), X (cross), D (dot), L (line)
        # Pozisyonlar: 1-4 (köşeler), H/V (yatay/dikey)
        
        self.encrypt_map = {
            'A': 'S1D',  # Square top-left with dot
            'B': 'S2D',  # Square top-right with dot
            'C': 'S3D',  # Square bottom-left with dot
            'D': 'S4D',  # Square bottom-right with dot
            'E': 'X1D',  # Cross top-left with dot
            'F': 'X2D',  # Cross top-right with dot
            'G': 'X3D',  # Cross bottom-left with dot
            'H': 'X4D',  # Cross bottom-right with dot
            'I': 'S1',   # Square top-left empty
            'J': 'S2',   # Square top-right empty
            'K': 'S3',   # Square bottom-left empty
            'L': 'S4',   # Square bottom-right empty
            'M': 'X1',   # Cross top-left empty
            'N': 'X2',   # Cross top-right empty
            'O': 'X3',   # Cross bottom-left empty
            'P': 'X4',   # Cross bottom-right empty
            'Q': 'S1L',  # Square top-left with line
            'R': 'S2L',  # Square top-right with line
            'S': 'S3L',  # Square bottom-left with line
            'T': 'S4L',  # Square bottom-right with line
            'U': 'X1L',  # Cross top-left with line
            'V': 'X2L',  # Cross top-right with line
            'W': 'X3L',  # Cross bottom-left with line
            'X': 'X4L',  # Cross bottom-right with line
            'Y': 'SP',   # Special symbol 1
            'Z': 'XP',   # Special symbol 2
        }
        
        # Ters harita (decrypt için)
        self.decrypt_map = {v: k for k, v in self.encrypt_map.items()}
    
    def encrypt(self, plaintext: str, key: str = None) -> str:
        """
        Metni Pigpen Cipher ile şifreler.
        
        Not: key parametresi bu algoritmada kullanılmaz (sadece arayüz uyumluluğu için).
        
        Adımlar:
        1. Her karakteri şablon koduna çevir
        2. Kodları birleştir (ayırıcı ile)
        
        Args:
            plaintext: Şifrelenecek metin
            key: Kullanılmaz (None)
        
        Returns:
            Şifreli metin (kodlar "|" ile ayrılmış)
        """
        # Metni hazırla
        text = prepare_text(plaintext, remove_spaces=True)
        
        # Her karakteri şablon koduna çevir
        ciphertext = []
        for char in text:
            if char in self.encrypt_map:
                ciphertext.append(self.encrypt_map[char])
            else:
                # Bilinmeyen karakter için boş
                ciphertext.append('??')
        
        # Kodları "|" ile birleştir
        return '|'.join(ciphertext)
    
    def decrypt(self, ciphertext: str, key: str = None) -> str:
        """
        Şifreli metni Pigpen Cipher ile çözer.
        
        Adımlar:
        1. Şifreli metni "|" ile ayır
        2. Her kodu karaktere çevir
        
        Args:
            ciphertext: Şifreli metin (kodlar "|" ile ayrılmış)
            key: Kullanılmaz (None)
        
        Returns:
            Çözülmüş metin
        """
        # Kodları ayır
        codes = ciphertext.split('|')
        
        # Her kodu karaktere çevir
        plaintext = []
        for code in codes:
            code = code.strip()
            if code in self.decrypt_map:
                plaintext.append(self.decrypt_map[code])
            else:
                # Bilinmeyen kod için "?" ekle
                plaintext.append('?')
        
        return ''.join(plaintext)

