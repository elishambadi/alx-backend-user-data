#!/usr/bin/env python3
"""
    Auth Module
"""
from flask import request
from typing import TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Wrapper to verify authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Checks Authorization headers"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current authorized user"""
        return None
