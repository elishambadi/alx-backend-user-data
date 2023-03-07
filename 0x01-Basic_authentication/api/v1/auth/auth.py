#!/usr/bin/env python
"""Basic Authentication Module
"""
from flask import Flask, jsonify, abort, request
from typing import List, TypeVar

app = Flask(__name__)


class Auth:
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required
        """
        if path is None:
            return True
        if path in excluded_paths or path+"/" in excluded_paths:
            return False
        else:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Checks Auth header and return it
        """
        if request is None:
            return None
        elif request.get("Authorization") is None:
            return None
        else:
            return request.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current user
        """
        return None
