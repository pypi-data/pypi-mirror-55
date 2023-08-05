#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : view.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

from ..config import main
from ..utils import view as _view


def view():
    _view(f'{main}.pdf')
