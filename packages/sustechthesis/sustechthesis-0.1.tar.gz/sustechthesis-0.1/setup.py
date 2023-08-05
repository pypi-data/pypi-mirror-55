#!/usr/bin/env python
# coding: utf-8
'''Set up package `sustechthesis`.
'''
import setuptools
import sustechthesis


with open('README.md', 'r') as f:
	long_description = f.read()

setuptools.setup(
	name='sustechthesis',
	version=sustechthesis.__version__,
	author='Iydon Liang',
	author_email='11711217@mail.sustech.edu.cn',
	license='MIT License',
	description='SUSTech Thesis',
	long_description=long_description,
	long_description_content_type='text/markdown',
	url='https://github.com/Iydon/pypi',
	packages=setuptools.find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3',
		'Environment :: Console',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
	],
	install_requires=[
		'click>=3.3',
	],
	entry_points={
		'console_scripts': [
			'sustechthesis = sustechthesis.__main__:cli',
		]
	}
)
