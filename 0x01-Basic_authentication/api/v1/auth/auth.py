#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""
    def require_auth(self,
                     path: str,
                     excluded_paths: List[str]) -> bool:
        """
        public method
        """
        if path is None or\
            excluded_paths is None or\
                  excluded_paths == []:
            return True
        if not path.endswith("/"):
            path += "/"
        if path not in excluded_paths:
            return True
        return False



    def authorization_header(self,
                             request=None) -> str:
        """
        public method
        """
        return None


    def current_user(self, request=None) -> TypeVar('User'):
        """
        public method
        """
        return None
