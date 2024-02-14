#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, TypeVar
from fnmatch import fnmatch


class Auth:
    """Auth class"""
    def require_auth(self,
                     path: str,
                     excluded_paths: List[str]) -> bool:
        """
        public method
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith("/"):
            path += "/"
        for ex_path in excluded_paths:
            if fnmatch(path, ex_path):
                return False
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self,
                             request=None) -> str:
        """
        public method
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        public method
        """
        return None
