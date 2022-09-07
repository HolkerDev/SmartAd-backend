import hashlib
import os


def hash_password(password: str) -> bytes:
    """Password encryption method"""
    salt: bytes = os.urandom(32)
    hashed_password: bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
    )
    return salt + hashed_password


def is_password_equals(old_password: bytes, password_to_check: str) -> bool:
    """Method checks if provided password is the same with old one"""
    salt: bytes = old_password[:32]
    old_key: bytes = old_password[32:]
    new_key: bytes = hashlib.pbkdf2_hmac(
        "sha256",
        password_to_check.encode("utf-8"),
        salt,
        100000,
    )
    return new_key == old_key
