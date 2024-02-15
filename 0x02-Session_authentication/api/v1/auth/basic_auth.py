#!/usr/bin/env python3
"""
BasicAuth class
"""
from models.user import User
from .auth import Auth
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """
        returns the Base64 part
        of the Authorization header
        """
        if authorization_header is None or \
            not isinstance(authorization_header, str) or \
                not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """
        Basic - Base64 decode
        """
        if base64_authorization_header is None or \
                not isinstance(base64_authorization_header, str):
            return None
        try:
            result = base64.b64decode(base64_authorization_header)
            return result.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Basic - User credentials
        """
        if decoded_base64_authorization_header is None or \
            not isinstance(decoded_base64_authorization_header, str) or \
                ':' not in decoded_base64_authorization_header:
            return None, None
        email = decoded_base64_authorization_header.split(":")[0]
        passworld = ":\
".join(decoded_base64_authorization_header.split(":")[1:])
        return email, passworld

    def user_object_from_credentials(
        self,
        user_email: str,
        user_pwd: str
    ) -> TypeVar('User'):
        """
        Basic - User object
        """
        if user_email is None or not isinstance(user_email, str) or \
                user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User().search({"email": user_email})
        if user == [] or not user[0].is_valid_password(user_pwd):
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Basic - Overload current_user - and BOOM!
        """
        author = self.authorization_header(request)
        authorBase64 = self.extract_base64_authorization_header(author)
        authorUtf8 = self.decode_base64_authorization_header(authorBase64)
        email, pwd = self.extract_user_credentials(authorUtf8)
        user = self.user_object_from_credentials(email, pwd)
        return user
