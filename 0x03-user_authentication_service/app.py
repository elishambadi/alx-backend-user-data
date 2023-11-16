#!/usr/bin/env python3
"""App module"""

from flask import Flask, jsonify, request
from flask import abort, make_response, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=["GET"])
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

        # Create a response object using jsonify
        response_body = jsonify({"email": email, "message": "logged in"})
        response = make_response(response_body, 200)

        # Set the session_id as a cookie in the response - 1 Day Max Age
        response.set_cookie("session_id", session_id)

        return response
    else:
        abort(401)


@app.route('/sessions', methods=["DELETE"])
def logout():
    """Logs Out a User"""
    session_id = request.cookies.get("session_id")

    if session_id is None:
        return redirect(url_for('index'))

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        response = redirect(url_for('index'))
        # Set a cookie in the response with immediate expiry
        response.set_cookie('session_id', '', expires=0)
        return response
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
