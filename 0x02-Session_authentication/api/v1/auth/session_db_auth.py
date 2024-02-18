#!/usr/bin/env python3
"""
session of authentication
"""
from .session_exp_auth import SessionExpAuth
import uuid
import os
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    session database authontication"""
    def create_session(self, user_id=None):
        """
        create session object
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(**{
            'session_id': session_id,
            'user_id': user_id
        })
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user_id for session
        """
        if session_id is None:
            return None
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if user_session is None or user_session == []:
            return None

        self.db_user = user_session[0]
        if super().user_id_for_session_id(session_id) is None:
            return None
        # UserSession.load_from_file()
        # user_session = UserSession.search({"session_id": session_id})
        # if user_session is None or user_session == []:
        #     return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        session destroy
        """
        if not super().destroy_session(request):
            return False
        session_id = self.session_cookie(request)
        try:
            user_session = UserSession.search({"session_id": session_id})
        except Exception:
            return None
        if user_session is None or user_session == []:
            return False
        user_session[0].remove()
        return True
