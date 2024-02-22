#!/usr/bin/env python3
"""
authentication methods
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB, NoResultFound
from typing import TypeVar
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        auth contractor method"""
        self._db = DB()

    def create_session(self, email) -> str:
        """
        session creation
        """
        user = self._db.find_user_by(email=email)
        user.session_id = _generate_uuid()
        return user.session_id

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """
        sign up and register a user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hp = _hash_password(password)
            user = self._db.add_user(email, hp)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """check if valid"""
        try:
            user = self._db.find_user_by(email=email)
            if checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False

    def get_user_from_session_id(self, session_id: str) -> TypeVar("User"):
        """
        Find user by session ID
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        user.reset_token = _generate_uuid()
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        self._db.update_user(
            user.id,
            hashed_password=_hash_password(password),
            reset_token=None
            )

    def destroy_session(self, user_id: int) -> None:
        """no more session"""
        self._db.update_user(user_id, session_id=None)


def _hash_password(pwd: str) -> bytes:
    """
    Hash password
    """
    return hashpw(pwd.encode('utf8'), gensalt())


def _generate_uuid() -> str:
    """
    generate a new uuid
    """
    return str(uuid.uuid4())
