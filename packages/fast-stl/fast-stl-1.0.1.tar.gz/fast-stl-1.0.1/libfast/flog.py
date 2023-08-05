# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-09-29.
# Copyright (c) 2019 3KWan.
# Description :
from libfast.decorator.singleton import Singleton


def log(content) -> None:
    print("some errors occurred in the fast-stl")
    print("error : " + str(content))


def logger():
    pass


@Singleton
class Logger:

    def __init__(self):
        pass
