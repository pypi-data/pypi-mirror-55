# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-31.
# Copyright (c) 2019 3KWan.
# Description :
import sqlite3
import atexit
from contextlib import contextmanager, closing
from pathlib import Path

_conn = None
_config = {}


def db_config(database: str, **kw) -> None:
    global _config
    kw["database"] = str(database)
    _config = kw


def connect() -> sqlite3.Connection:
    global _conn
    if not _conn:
        _conn = sqlite3.connect(**_config)
        atexit.register(_conn.close())
    return _conn


@contextmanager
def trans():
    try:
        conn = connect()
        yield
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def execute(sql: str, params: list = None):
    if params is None:
        params = []
    return connect().execute(sql, params)


def executemany(sql: str, params: list = None):
    if params is None:
        params = []
    return connect().executemany(sql, params)


def executescript(sql: str):
    return connect().executescript(sql)


def executefile(pkg: str, filename: str):
    from pkgutil import get_data

    data = get_data(pkg, filename)
    sql = data.decode("utf-8")
    return executescript(sql)


def find(sql: str, params: list = None, multi=True):
    if params is None:
        params = []
    cur = execute(sql, params)
    with closing(cur):
        return cur.fetchall() if multi else cur.fetchone()


def findone(sql: str, params: list = None):
    if params is None:
        params = []
    row = findone(sql, params)
    return row and row[0]


def findvalue(sql: str, params=None):
    if params is None:
        params = []
    row = findone(sql, params)
    return row and row[0]
