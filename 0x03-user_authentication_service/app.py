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
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    """
    go back to home page
    """
    return redirect('/')


@app.route("/profile", methods=['GET'])
def profile():
    """log out"""
    session_ID = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_ID)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """get token for resting password"""
    email = request.form.get("email")
    try:
        tk = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": tk}), 200


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """PUT /reset_password"""
    email = request.form.get("email")
    tk = request.form.get("reset_token")
    pw = request.form.get("new_password")
    try:
        AUTH.update_password(tk, pw)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
