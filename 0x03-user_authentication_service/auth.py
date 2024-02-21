#!/usr/bin/env python3
"""
authentication methods
"""
from bcrypt import hashpw, gensalt
from db import DB, NoResultFound
from typing import TypeVar


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """
        auth contractor method"""
        self._db = DB()

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


def _hash_password(pwd: str) -> bytes:
    """
    Hash password
    """
    return hashpw(pwd.encode('utf8'), gensalt())
