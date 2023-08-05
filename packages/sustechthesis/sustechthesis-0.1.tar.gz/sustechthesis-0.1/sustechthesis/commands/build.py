#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : build.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from ..config import main
from ..utils import latexmk


def build():
    latexmk(main, run=True, xelatex=None)
