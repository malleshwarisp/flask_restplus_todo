import os
import hashlib


def hash_password(password: str, salt: bytes = None):
    if not salt:
        salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return salt + key


def check_password(password: str, hash: bytes):
    new_hash = hash_password(password, hash[:32])
    return new_hash == hash
