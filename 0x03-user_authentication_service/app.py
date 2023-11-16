#!/usr/bin/env python3
"""App module"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index():
    """Home Route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=["POST"])
def users():
    """
    Route to register a user
    Implements: register_user from auth
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": f"{user.email}",
            "message": "user created"
            }), 200
    except Exception as exc:
        print(exc)
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login():
    """Logs in a user and creates a new session"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(401)

    valid_login = AUTH.valid_login(email, password)

    if valid_login:
        session_id = AUTH.create_session(email)

        # #  Make response and set a cookie
        # resp = make_response()
        # resp.set_cookie("session_id", session_id)

        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie("session_id", session_id)

        return response
    else:
        abort(401)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
