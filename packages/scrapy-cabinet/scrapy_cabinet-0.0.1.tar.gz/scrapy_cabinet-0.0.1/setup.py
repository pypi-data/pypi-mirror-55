# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 16:16
# @E-Mail  : aberstone.hk@gmail.com
# @File    : setup.py
# @Software: PyCharm
import os
from setuptools import setup, find_packages

about = {}
with open(os.path.join('scrapy_cabinet', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=read_file("README.md"),
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    install_requires=read_requirements("requirements.txt"),
    license=about['__license__'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
if __name__ == '__main__':
    packages = find_packages()
    print(packages)
