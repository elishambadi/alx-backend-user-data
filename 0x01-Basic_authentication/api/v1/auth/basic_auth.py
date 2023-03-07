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
