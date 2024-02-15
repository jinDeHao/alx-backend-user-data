#!/usr/bin/env python3
"""
session of authentication
"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """
    authentication session
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a session"""
        if user_id is None or not isinstance(user_id, str):
            return None
        Session_id = str(uuid.uuid4())
        self.user_id_by_session_id[Session_id] = user_id
        return Session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        User ID for Session ID
        """
        return None if session_id is None or\
            not isinstance(session_id, str)\
            else self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Use Session ID for identifying a User
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Logout
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
