import hashlib


def get_hash(original: str) -> str:
    m = hashlib.sha256()
    m.update(original.encode("utf-8"))
    return m.hexdigest()
