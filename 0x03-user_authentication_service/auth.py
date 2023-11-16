#!/usr/bin/env python3
"""Auth module"""
import bcrypt

def _hash_password(password: str)->bytes:
    """Hashes a password using bcrypt and returns bytes"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt)