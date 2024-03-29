#!/usr/bin/env python3
"""
    Auth Module
"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Wrapper to verify authentication"""

        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True

        # Appending a slash to each path
        if path.endswith('/'):
            pass
        else:
            path = path+"/"

        # Checking wildcard paths
        for exc_path in excluded_paths:

            if exc_path.endswith("*"):
                if exc_path[:-1] in path:
                    return False

        if path not in excluded_paths:
            return True
        elif path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """Checks Authorization headers"""
        if request is None:
            return None
        elif request.headers.get("Authorization") is None:
            return None
        else:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current authorized user"""
        return None
