# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-08.
# Copyright (c) 2019 3KWan.
# Description :

from libfast import fcmd
from libfast.fcfg import Config, write_option_value
from libfast.fmd5 import get_file_md5
from libfast.flog import Logger

if __name__ == "__main__":
    options = ["username", "password", "remember_flag"]
    cfg = Config("/Users/Suyghur/Develop/fast-str/test_log.cfg")
    cfg2 = Config("/Users/Suyghur/Develop/fast-str/test_log.cfg")

    print(write_option_value("/Users/Suyghur/Develop/fast-str/aaa.cfg", "aaa", "bbb", "ccc"))
    print(cfg2)
