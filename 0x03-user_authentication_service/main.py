#!/usr/bin/env python3
"""
Main file
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """new regiter"""
    url = "http://127.0.0.1:5000/users"
    response = requests.post(url,
                             data={"email": email, "password": password})
    assert response.status_code == 200 and\
        response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in wrong password"""
    pass


def log_in(email: str, password: str) -> str:
    """log in"""
    pass


def profile_unlogged() -> None:
    """
    profile unlogged
    """
    pass


def profile_logged(session_id: str) -> None:
    """
    profile logged
    """
    pass


def log_out(session_id: str) -> None:
    """log out"""
    pass


def reset_password_token(email: str) -> str:
    """reset passwd token"""
    pass


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update passwd"""
    pass


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
