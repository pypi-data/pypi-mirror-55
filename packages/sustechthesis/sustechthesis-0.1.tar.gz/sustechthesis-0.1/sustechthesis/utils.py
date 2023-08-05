#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : utils.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : <no docstring>
'''

import os
import webbrowser


def latexmk(*args, run=False, **kwargs):
    '''Latexmk: Automatic LaTeX document generation routine.

    Argument
    --------
    run: bool, whether to run the command
    args: tuple, arguments of latexmk
    kwargs: dict, arguments of latexmk

    Example
    -------
    >>> latexmk('main', xelatex=None, print='pdf', f_=None)
    latexmk -xelatex -print=pdf -f- main
    '''
    def _parse_option(key, val):
        _key = key.replace('_', '-')
        if val is not None:
            return f'-{_key}={val}'
        else:
            return f'-{_key}'

    opt = [_parse_option(k, v) for k, v in kwargs.items()]
    cmd = f'latexmk {" ".join(opt)} {" ".join(args)}'
    if run:
        os.system(cmd)
    return cmd


def view(target_link):
    '''Use browser to view pdf or link.
    '''
    return webbrowser.open(target_link)


def exists(path):
    '''Test whether a path exists.
    '''
    return os.path.exists(path)
