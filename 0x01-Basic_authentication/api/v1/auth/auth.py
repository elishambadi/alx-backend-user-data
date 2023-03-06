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
        """Require authentication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """Checks Auth header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current user
        """
        return None
