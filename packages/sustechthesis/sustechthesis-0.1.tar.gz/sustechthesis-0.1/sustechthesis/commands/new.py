#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : new.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from ..config import content, main
from ..utils import exists


def new():
    file = f'{main}.tex'
    if exists(file):
        print('File already exists.')
    else:
        with open(file, 'w') as f:
            f.write(content)
