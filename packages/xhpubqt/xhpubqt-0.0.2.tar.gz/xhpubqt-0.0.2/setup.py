# -*- coding:utf-8 -*-
'''
@Author: lamborghini1993
@Date: 2019-09-29 17:41:58
@UpdateDate: 2019-11-06 17:11:17
@Description: 发布包的配置
    https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives
'''

import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setup(
    name='xhpubqt',
    version="0.0.2",
    author="lamborghini1993",
    author_email="1323242382@qq.com",
    description='a pub library for PyQt5 to implement some cool controls',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/lamborghini1993/mypypi/tree/master/xhpubqt',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
