#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

if os.getenv('AUTH_TYPE'):
    auth = os.getenv('AUTH_TYPE')


if str(auth) == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif str(auth) == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """

    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """

    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """
        Runs before request to check authorization headers
        Returns:
        - Abort if request is not authorized/authenticated
    """
    excluded_paths = [
        '/api/v1/stat*',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
        ]
    if auth is None:
        pass

    if auth.require_auth(request.path, excluded_paths) is False:
        pass
    else:
        if auth.authorization_header(request) is None:
            abort(401)
        elif auth.current_user(request) is None:
            abort(403)

    request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
