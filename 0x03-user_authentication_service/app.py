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
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route('/profile', methods=["GET"])
def profile():
    """Returns a users profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    if user:
        return jsonify({"email": f"{user.email}"})


@app.route('/reset_password', method=["POST"])
def get_reset_password_token():
    """Reset token password"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})
    except ValueError as exc:
        #  If get_reset_password_token gets no user...
        #  It will throw a ValueError which we intercept here
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
