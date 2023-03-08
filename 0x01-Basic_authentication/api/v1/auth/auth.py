#!/usr/bin/env python3
"""Basic Authentication Module
"""
from flask import Flask, jsonify, abort, request
from typing import List, TypeVar

app = Flask(__name__)


class Auth:
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path is in paths paths excluded from auth.
           Auth is only false if path is in list of excluded paths.

           Returns:
            - True auth required
            - False auth not required
        """
        # print("Excluded: {}".format(excluded_paths))
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths or path+"/" in excluded_paths:
            return False
        else:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """Checks Auth header and return it
        """
        headers = dict(request.headers)
        if request is None:
            return None
        elif headers.get("Authorization") is None:
            return None
        else:
            return headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current user
        """
        return None
