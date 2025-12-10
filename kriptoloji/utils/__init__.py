"""
Kriptoloji Yardımcı Modülleri
Matris ve metin işleme fonksiyonları.
"""

from .matrix_utils import (
    create_matrix,
    matrix_multiply,
    matrix_determinant,
    matrix_inverse,
    mod_inverse,
    text_to_matrix,
    matrix_to_text
)

from .text_utils import (
    prepare_text,
    split_into_blocks,
    remove_duplicates,
    char_to_index,
    index_to_char,
    pad_text
)

__all__ = [
    'create_matrix',
    'matrix_multiply',
    'matrix_determinant',
    'matrix_inverse',
    'mod_inverse',
    'text_to_matrix',
    'matrix_to_text',
    'prepare_text',
    'split_into_blocks',
    'remove_duplicates',
    'char_to_index',
    'index_to_char',
    'pad_text',
]

