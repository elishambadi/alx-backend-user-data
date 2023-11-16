#!/usr/bin/env python3
"""App module"""

from flask import Flask, jsonify, request
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
    password = request.form.get("email")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({
            "email": f"{user.email}",
            "message": "user created"
            }), 200
    except Exception as exc:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
