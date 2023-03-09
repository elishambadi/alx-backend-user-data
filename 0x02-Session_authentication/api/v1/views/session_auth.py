#!/usr/bin/env python3
""" Module of Users views
"""
import os
import sys
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
sys.path.append("""/home/elisha/Documents/ALX/alx-backend-user-data/
                   0x02-Session_authentication/""")


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_login():
    """Authenticated login requests
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    elif password is None or len(email) == 0:
        return jsonify({"error": "password missing"}), 400
    else:
        user_ = User.search({"email": email})

    if user_ is None or len(user_) == 0:
        return jsonify({"error": "no user found for this email"})
    else:
        user_ = user_[0]

    if user_.is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user_.id)
        resp = make_response(user_.to_json())
        resp.set_cookie(os.getenv("SESSION_NAME"), session_id)
        return resp
