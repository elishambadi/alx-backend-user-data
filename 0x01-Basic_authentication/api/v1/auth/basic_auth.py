#!/usr/bin/env python3
"""
    BasicAuth Module
"""
from flask import request
from typing import TypeVar, List
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth that inherits from Auth"""
    pass
