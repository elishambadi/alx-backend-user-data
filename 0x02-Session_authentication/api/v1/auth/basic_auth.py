#!/usr/bin/env python3
"""Basic Auth inheriting from Auth
"""
import base64
import re
from .auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(self, auth_header: str) -> str:
        """Extracts and return base 64 part of the code
           e.g. >> str = "Authorization: Basic afsfnkwnkjfnknrfi23u4uh92j"
                >> auth = BasicAuth()
                >> print(auth.extract_base64_authorization_header(str))
                >> "afsfnkwnkjfnknrfi23u4uh92j"
        """
        if type(auth_header) != str:
            return None
        else:
            match = re.search(r'^Basic\s+(.*)$', auth_header)

            if match:
                return match.group(1)
            else:
                return None

    def decode_base64_authorization_header(
            self,
            base64_auth_header: str
            ) -> str:
        """Decode base64 value
        """
        if base64_auth_header is None:
            return None
        elif type(base64_auth_header) != str:
            return None

        try:
            result = base64.b64decode(base64_auth_header).decode('utf-8')
            return result
        except Exception as exc:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """Extract user credentials as tuple
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif type(decoded_base64_authorization_header) != str:
            return (None, None)
        elif ':' not in decoded_base64_authorization_header:
            return (None, None)
        else:
            """ Decode the string  """
            match = re.search(r':(.+)$', decoded_base64_authorization_header)
            email = decoded_base64_authorization_header.split(':')[0]
            if match:
                pass_ = match.group(0)[1:]
            return (email, pass_)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        """Create a user object from the credentials
        """
        if type(user_email) != str:
            return None
        elif type(user_pwd) != str or user_pwd is None:
            return None
        elif len(User.search({"email": user_email})) == 0:
            return None
        else:
            user_ = User.search({"email": user_email})[0]

        if user_.is_valid_password(user_pwd) is not True:
            return None
        else:
            return user_

    def current_user(self, request=None) -> TypeVar('User'):
        """Return the current auth user
        """
        auth_header = self.authorization_header(request)
        base_64 = self.extract_base64_authorization_header(auth_header)
        decoded_base_64 = self.decode_base64_authorization_header(base_64)
        user_cred = self.extract_user_credentials(decoded_base_64)
        user_ = self.user_object_from_credentials(user_cred[0], user_cred[1])

        return user_
