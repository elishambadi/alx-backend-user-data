#!/usr/bin/env python3
"""Auth module"""
import bcrypt

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns bytes"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""
        if email is None:
            return None
        if password is None:
            return None

        user = None
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            pass
        if user is not None:
            raise ValueError(f"User {email} already exists")
        else:
            # Create a new user
            hashed_pw = _hash_password(password)

            user = self._db.add_user(email, hashed_pw)
            return user
