# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-31.
# Copyright (c) 2019 3KWan.
# Description :
import sqlite3
from typing import Any

from libfast.fio import exists, isfile
from libfast.flog import log


class BaseSqlite:
    SHOW_SQL = True

    def __init__(self, path: str):
        self.path = path

    def get_conn(self) -> Any:
        try:

            if exists(self.path) and isfile(self.path):
                print("database path : " + self.path)
                conn = sqlite3.connect(self.path)
                conn.text_factory = str
                return conn
            else:
                return None
        except Exception as e:
            log(e)
            return None
