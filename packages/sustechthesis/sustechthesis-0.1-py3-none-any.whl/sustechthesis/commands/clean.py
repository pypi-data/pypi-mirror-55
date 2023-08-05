#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : clean.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from ..utils import latexmk


def clean():
    latexmk(run=True, c=None)
