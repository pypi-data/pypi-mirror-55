# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-08.
# Copyright (c) 2019 3KWan.
# Description :
import hashlib

from build.lib.libfast.flog import log
from libfast.fio import exists


def get_file_md5(file_path) -> str:
    """
    计算文件的md5
    :param file_path: 文件路径
    :return: md5 code
    """
    try:
        f = open(file_path, "rb")
        md5_obj = hashlib.md5()
        while True:
            d = f.read(8096)
            if not d:
                break
            md5_obj.update(d)
        hash_code = md5_obj.hexdigest()
        f.close()
        md5 = str(hash_code).lower()
        return md5
    except Exception as e:
        log(e)
        return ""


def compare_md5(file_path, target_md5) -> bool:
    """
    md5值校验
    :param file_path: 文件路径
    :param target_md5: 目标md5
    :return: bool
    """
    try:
        if exists(file_path):
            res_md5 = get_file_md5(file_path)
            if res_md5 == target_md5:
                return True
        else:
            return False
    except Exception as e:
        log(e)
        return False
