from hashlib import sha256


def hash_string(string: str) -> str:
    """Hash a string with sha256 algorithm."""
    hash_func = sha256()
    hash_func.update(string.encode())
    return hash_func.hexdigest()
