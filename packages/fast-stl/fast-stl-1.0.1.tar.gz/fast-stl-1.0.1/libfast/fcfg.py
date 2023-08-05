# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-10-18.
# Copyright (c) 2019 3KWan.
# Description :
from configparser import ConfigParser
from typing import Any

from libfast.decorator.singleton import Singleton
from libfast.fio import exists


@Singleton
class Config:
    __cfg = None

    def __init__(self, path):
        if exists(path):
            self.__cfg = ConfigParser()
            self.__cfg.read(path, encoding="UTF-8")

    @property
    def cfg(self) -> Any:
        return self.__cfg


def get_config_instance(path: str) -> Any:
    return Config(path).cfg


def read_option_value(path: str, section: str, key: str) -> str:
    """
    读取单个key
    :param path: cfg文件路径
    :param section:  节点名称
    :param key: 关键字
    :return: 对应值
    """
    return get_config_instance(path).get(section, key)


def read_options_value(path: str, section: str, keys: list) -> dict:
    """
    读取多个key
    :param path: cfg文件路径
    :param section: 节点名称
    :param keys: 关键字列表
    :return: value字典
    """
    values = dict()
    for key in keys:
        values[key] = read_option_value(path, section, key)
    return values


def write_option_value(path: str, section: str, key: str, value: str) -> bool:
    cfg = get_config_instance(path)
    if section not in cfg.sections():
        cfg.add_section(section)
    cfg.set(section, key, value)
    with open(path, "w", encoding="UTF-0") as f:
        cfg.write(f)
        return True
