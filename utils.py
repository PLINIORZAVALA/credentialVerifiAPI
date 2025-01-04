"""
Funciones auxiliares para generación y validación de firmas.
"""

import hashlib

def generate_signature(data: str) -> str:
    """Genera una firma digital hash basada en los datos proporcionados."""
    return hashlib.sha256(data.encode()).hexdigest()
