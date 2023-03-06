#!/usr/bin/env python3
from flask import render_template, abort, Flask, request, jsonify

app = Flask(__name__)
@app.route('/api/v1/unauthorized', methods=["GET"])
def unauthorized():
   return abort(401, description="Unauthorized")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="4800")
