#!/usr/bin/env python3
"""Session Authentication module
"""
import uuid
import os
from .auth import Auth


class SessionAuth(Auth):
    """SessionAuth Class Definition
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session
        """
        if user_id is None:
            return None
        elif type(user_id) != str:
            return None
        else:
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id.update({session_id: user_id})
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user id based on session id
        """
        if session_id is None:
            return None
        elif type(session_id) != str:
            return None
        else:
            return self.user_id_by_session_id.get(session_id)
