#!/usr/bin/env python3
"""Basic Auth inheriting from Auth
"""
import base64
import re
from .auth import Auth


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
            return tuple(decoded_base64_authorization_header.split(":"))
