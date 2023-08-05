#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
@File      : __main__.py
@Time      : 2019/11/04
@Author    : Iydon Liang
@Contact   : liangiydon@gmail.com
@Docstring : \\
	1. Use `logging` module.
	2. Add more options and configurations.
'''
assert __package__, 'Please use `-m` option.'

import click
import os
import sys
from . import __version__
from .commands import doc, new, build, view, issue, clean


pkg_dir = os.path.dirname(os.path.abspath(__file__))

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(
	'{0} from {1} (Python {2})'.format(__version__, pkg_dir, sys.version[:3]),
	'-V', '--version')
def cli():
	'''SUSTechThesis - SUSTech Thesis.
	'''

@cli.command(name='doc')
def doc_command():
	'''View the documentation of SUSTech Thesis.
	'''
	doc.doc()

@cli.command(name='new')
def new_command():
	'''Initialize SUSTech Thesis Project.
	'''
	new.new()

@cli.command(name='build')
def build_command():
	'''Build SUSTech Thesis via `latexmk`
	'''
	build.build()

@cli.command(name='view')
def view_command():
	'''View the result PDF after compiling
	'''
	view.view()

@cli.command(name='clean')
def clean_command():
	'''Clean the cache file.
	'''
	clean.clean()

@cli.command(name='issue')
def issue_command():
	'''Issue.
	'''
	issue.issue()
