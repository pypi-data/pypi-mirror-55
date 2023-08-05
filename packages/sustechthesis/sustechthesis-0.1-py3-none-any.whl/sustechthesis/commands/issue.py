#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : issue.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from ..config import issues
from ..utils import view


def issue():
    for i in issues:
        view(i)
