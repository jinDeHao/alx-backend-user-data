#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get("email")
    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400
    """get the user from the database using the email"""
    user_list = User.search({'email': email})
    user = user_list[0]
    """check if the user exists"""
    if not user_list:
        return jsonify({"error": "no user found for this email"}), 404
    """check if the password is valid"""
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.auth.session_auth import SessionAuth
    """create a session for a user"""
    session_id = SessionAuth().create_session(user.id)
    """get the session name from variable envirenement"""
    SESSION_NAME = os.getenv("SESSION_NAME")
    """make a response using user data"""
    response = make_response(user.to_json())
    """set a cookie for the session id"""
    response.set_cookie(key=SESSION_NAME, value=session_id)
    return response
