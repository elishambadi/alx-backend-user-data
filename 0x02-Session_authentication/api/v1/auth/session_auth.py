#!/usr/bin/env python3
"""Session Authentication module
"""
import uuid
import os
from .auth import Auth
import sys
from models.user import User

sys.path.append("""/home/elisha/Documents/ALX/alx-backend-user-data/
                 0x02-Session_authentication/""")


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

    def current_user(self, request=None):
        """Returns a user instance
        """
        cookie_val = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_val)
        print("Cookie val: {}, user_id: {}".format(cookie_val, user_id))
        return User.get(user_id)

    def destroy_session(self, request=None):
        if request is None:
            return False
        elif self.session_cookie(request) is None:
            return False
        elif len(User.search(self.user_id_for_session_id(self.session_cookie(request)))) == 0:
            return False
        else:
            del self.user_id_by_session_id[self.session_cookie(request)]
