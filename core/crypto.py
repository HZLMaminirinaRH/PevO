"""Utilities partagées pour le chiffrement XOR entre les nœuds"""

XOR_KEY = 0x42

def appliquer_xor(donnees_str):
    """Chiffre une chaîne avec XOR"""
    return bytes([b ^ XOR_KEY for b in donnees_str.encode('utf-8')])

def dechiffrer_xor(donnees_bytes):
    """Déchiffre des bytes avec XOR"""
    return "".join([chr(b ^ XOR_KEY) for b in donnees_bytes])
