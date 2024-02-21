#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import TypeVar


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(
            self,
            email: str,
            hashed_password: str) -> User:
        """
        adds a new user
        """
        user = User(email=email,
                    hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **args: dict) -> User:
        """
        Find user by his attributes
        """
        try:
            user = self._session.query(User).filter_by(**args).first()
        except Exception:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self,
                    user_id: int,
                    **args: dict) -> None:
        """
        update a targeted user
        """
        targeted_user = self.find_user_by(**{"id": user_id})
        for key, val in args.items():
            if hasattr(targeted_user, key):
                if val is None or\
                        type(getattr(targeted_user, key)) is type(val):
                    setattr(targeted_user, key, val)
                    continue
            raise ValueError
        self._session.commit()
