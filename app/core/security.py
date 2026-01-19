import hashlib

def verify_meridian_key(plain_key: str, hashed_key: str) -> bool:
    """Compara la key enviada por el BDR con el hash en la DB"""
    incoming_hash = hashlib.sha256(plain_key.encode()).hexdigest()
    return incoming_hash == hashed_key