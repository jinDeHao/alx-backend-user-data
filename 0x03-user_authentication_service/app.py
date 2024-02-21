#!/usr/bin/env python3

from flask import Flask, request, jsonify, abort, make_response, redirect
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=['GET'])
def wellcome():
    """salut"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """sign up"""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """log in"""
    email, password = request.form.get("email"), request.form.get("password")
    if AUTH.valid_login(email, password):
        session_ID = AUTH.create_session(email)
        responce = make_response({"email": email, "message": "logged in"})
        responce.set_cookie("session_id", session_ID)
        return responce
    else:
        abort(401)


@app.route("/sessions", methods=['DELETE'])
def logout():
    """log out"""
    session_ID = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_ID)
    AUTH.destroy_session(user.id)
    """
    go back to home page
    """
    redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
