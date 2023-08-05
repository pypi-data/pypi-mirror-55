# _*_coding:utf-8_*_
# Created by #Suyghur, on 2019-09-30.
# Copyright (c) 2019 3KWan.
# Description :
import subprocess


def exec_cmd_line(bash_script):
    p = subprocess.Popen(bash_script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         universal_newlines=True)
    status = p.wait()
    for line in p.stdout.readlines():
        print(line)
    return status
