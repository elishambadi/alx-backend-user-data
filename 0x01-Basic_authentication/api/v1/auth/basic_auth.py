#!/usr/bin/env python3
"""
    BasicAuth Module
"""
import base64
from flask import request
from typing import TypeVar, List
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """BasicAuth that inherits from Auth"""
    pass

    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
            returns the Base64 part of the Authorization header
        """

        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif authorization_header.startswith("Basic ") is False:
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """Decodes the base64 header that has been extracted"""
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_header = base64.b64decode(base64_authorization_header)
            header_text = decoded_header.decode('utf-8')
            return header_text
        except Exception as exc:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
            Extracts user credentials from the extracted header text
        """
        if decoded_base64_authorization_header is None:
            return None, None
        elif not isinstance(decoded_base64_authorization_header, str):
            return None, None
        elif ":" not in decoded_base64_authorization_header:
            return None, None
        else:
            name, email = decoded_base64_authorization_header.split(":")
            return name, email

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """Returns a created user object from username and email"""
        if user_email is None or not isinstance(user_email, str):
            return None
        elif user_pwd is None or not isinstance(user_pwd, str):
            return None
        else:
            users = []
            if User.search({"email": user_email}) == []:
                # If no users match return None
                return None
            else:
                # Store a list of all user objects matching email
                users = User.search({"email": user_email})
                for user in users:

                    if user.is_valid_password(user_pwd):  # Checks password
                        return user
                    else:
                        return None
