# -*- coding: utf-8 -*-

"""Connection to database
"""
import abc
from collections import defaultdict
from contextlib import contextmanager

import psycopg2
from sqlalchemy import create_engine
import sqlite3

__all__ = [
    "SQLiteConnector",
    "PgConnector"
]


class BaseConnector(abc.ABC):
    """Definition of basic connection parameters.

    Attributes:
        conn:
            An instance of `psycopg2` connection object.
        engine:
            An instance of `SQLAlchemy` engine object.
    """

    def __init__(self, **kwargs):
        self.conn = None
        self.engine = None

    def __del__(self):
        self.close_connection()

    @abc.abstractmethod
    def make_engine(self):
        raise NotImplementedError()

    @contextmanager
    def make_connection(self):
        if self.conn is None:
            self.set_connection()

        yield self.conn

        self.close_connection()

    @abc.abstractmethod
    def set_connection(self, **kwargs):
        raise NotImplementedError()

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None


class SQLiteConnector(BaseConnector):
    """Setting a connection with SQLite database.

    Args:
        path2db:
            Path to database file.
    """

    def __init__(self, path2db: str) -> None:
        super().__init__()

        self.path2db = path2db
        self.engine = self.make_engine()

    def make_engine(self):
        return create_engine('sqlite:///' + self.path2db, echo=False)

    def set_connection(self):
        self.conn = sqlite3.connect(self.path2db)


class PgConnector(BaseConnector):
    """Setting a connection with database.

    Besides the basic connection parameters any other
    connection parameter supported by `psycopg2.connect`
    can be passed as a keyword.

    Args:
        host:
            Database host address.
        port:
            Connection port number.
        user:
            User name.
        password:
            User password.
        db_name:
            The database name.

    Keyword args:
        schema:
            If schema is specified, then setting a connection to the schema only.

    Example:

          .. code::

          >>> conn = PgConnector('localhost', '5432', 'postgres', 'password', 'test_db')

    """

    def __init__(
            self,
            host: str,
            port: str,
            user: str,
            password: str,
            db_name: str,
            **kwargs: str
    ) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.schema = kwargs.get('schema', None)

        self.conn_params = defaultdict()

        for key in kwargs.keys():
            if key not in ['schema']:
                self.conn_params[key] = kwargs.get(key)

        self.engine = self.make_engine()

    def make_engine(self):
        """Create `SQLAlchemy` engine.
        """

        engine = 'postgresql://' + \
                 self.user + ':' + \
                 self.password + '@' + \
                 self.host + ':' + \
                 self.port + '/' + \
                 self.db_name

        for key in self.conn_params.keys():
            engine += '?' + key + '=' + self.conn_params[key]

        connect_args = defaultdict()

        if self.schema is not None:
            connect_args['options'] = '-csearch_path=' + self.schema

        return create_engine(engine, connect_args=connect_args)

    def set_connection(self, **kwargs):
        """Setting `psycopg2` connection.
        """

        conn_params = self.conn_params
        conn_params['host'] = self.host
        conn_params['port'] = self.port
        conn_params['user'] = self.user
        conn_params['password'] = self.password
        conn_params['dbname'] = self.db_name
        
        if self.schema is not None:
            conn_params['options'] = f'--search_path={self.schema}'

        self.conn = psycopg2.connect(**conn_params)
