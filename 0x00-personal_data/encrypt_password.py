#!/usr/bin/env python3
"""Hashes password using bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password
       Example:
       >> password = "MyAmazingPassw0rd"
       >> print(hash_password(password))
       >> b'$2b$12$xSAw.bxfSTAlIBglPMXeL.SJnzme3Gm0E7eOEKOVV2OhqOakyUN5m'
    """
    pass_ = bytes(password, 'utf-8')
    return bcrypt.hashpw(pass_, bcrypt.gensalt())
