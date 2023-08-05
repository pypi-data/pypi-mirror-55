# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-09-29.
# Copyright (c) 2019 3KWan.
# Description :
import os
import shutil

from libfast.flog import log


def exists(target: str) -> bool:
    """
    判断源文件或源文件夹路径
    :param target: 源文件或源文件夹路径
    :return: 是否存在
    """
    try:
        if os.path.exists(target):
            return True
        else:
            return False
    except Exception as e:
        log(e)
        return False


def isfile(target: str) -> bool:
    """
    判断源文件是否文件
    :param target: 源文件
    :return: 是否文件
    """
    try:
        if exists(target):
            return os.path.isfile(target)
        else:
            return False
    except Exception as e:
        log(e)
        return False


def isdir(target: str) -> bool:
    """
    判断源路径是否目录
    :param target: 源路径
    :return: 是否目录
    """
    try:
        if exists(target):
            return os.path.isdir(target)
        else:
            return False
    except Exception as e:
        log(e)
        return False


def create_dir(target: str) -> bool:
    """
    创建目录
    :param target: 源文件或源文件夹路径
    :return: 是否成功
    """
    try:
        if not exists(target):
            os.makedirs(target)
            return True
        else:
            log("target is existed")
            return False
    except Exception as e:
        log(e)
        return False


def copy_files(res: str, target: str) -> bool:
    """
    拷贝文件或文件夹
    :param res: 源文件或源文件夹路径
    :param target: 目标路径
    :return: 是否成功
    """
    try:
        if isfile(res):
            shutil.copy(res, target)
            return True
        else:
            if exists(target):
                for file in os.listdir(res):
                    shutil.copy(res + "/" + file, target)
            else:
                shutil.copytree(res, target)
            return True
    except Exception as e:
        log(e)
        return False


def remove_files(target: str) -> bool:
    """
    删除文件或文件夹
    :param target: 目标文件或文件夹路径
    :return: 是否成功
    """
    try:
        if isfile(target):
            os.remove(target)
            return True
        else:
            shutil.rmtree(target)
            return True
    except Exception as e:
        log(e)
        return False


def rename_file(target: str, new_name: str) -> bool:
    """
    重命名文件
    :param target: 目标文件或文件夹路径
    :param new_name: 新名称
    :return: 是否成功
    """
    try:
        if exists(target):
            os.rename(target, new_name)
            return True
        else:
            log("target does not exist")
    except Exception as e:
        log(e)
        return False


def replace_file_content(res: str, old_tag: str, new_tag: str) -> bool:
    """
    修改可读文件中预定义的标记值
    :param res: 文件路径
    :param old_tag: 预定义的标记
    :param new_tag: 需要替换的标记
    :return: 是否成功
    """
    try:
        with open(res, "r", encoding="utf-8") as f:
            content = f.read().replace(old_tag, new_tag)
        with open(res, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        log(e)
        return False
