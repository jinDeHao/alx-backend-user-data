#!/usr/bin/env python3
"""
session of authentication
"""
from .auth import Auth
import uuid


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
