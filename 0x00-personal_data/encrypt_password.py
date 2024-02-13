#!/usr/bin/env python3
"""
Encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    I use the bcrypt package to perform
    the hashing (with hashpw).
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password) -> bool:
    """
    Check valid password
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
