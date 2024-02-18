#!/usr/bin/env python3
"""
session of authentication
"""
from .session_auth import SessionAuth
import uuid
from models.user import User
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    authentication session
    """
    def __init__(self):
        """
        constrator method
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create session for user
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        diction = {}
        diction['user_id'] = user_id
        diction['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = diction
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            if hasattr(self, "db_user"):
                diction = {}
                diction['user_id'] = self.db_user.id
                diction['created_at'] = self.db_user.created_at
                self.user_id_by_session_id[session_id] = diction
            else:
                return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id[session_id]["user_id"]
        if "created_at" not in self.user_id_by_session_id[session_id]:
            return None
        time_change = timedelta(seconds=self.session_duration)
        new_time = self.user_id_by_session_id[session_id]["\
created_at"] + time_change
        if new_time <= datetime.now():
            return None
        return self.user_id_by_session_id[session_id]["user_id"]
