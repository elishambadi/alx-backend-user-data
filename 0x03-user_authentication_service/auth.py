#!/usr/bin/env python3
"""Auth module"""
import bcrypt
import uuid

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt and returns bytes"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    """Generates a UUID"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Logs in a user"""
        if email is None:
            return None
        if password is None:
            return None

        try:
            user = self._db.find_user_by(email=email)
        except Exception as exc:
            return False

        bytes = password.encode('utf-8')

        #  Check user password using bcrypt
        if bcrypt.checkpw(bytes, user.hashed_password):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """
            Generates a sessionID from email

            Args:
                email (str): user email

            Returns:
                Session ID (str): A new session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception as exc:
            #  Incase of error return None
            return None

        new_uuid = _generate_uuid()
        try:
            self._db.update_user(user.id, session_id=new_uuid)
            return new_uuid
        except Exception as exc:
            #  Incase of error return None
            return None
