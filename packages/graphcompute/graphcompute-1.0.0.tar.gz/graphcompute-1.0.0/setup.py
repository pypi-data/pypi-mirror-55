#!/usr/bin/env python

import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = ''
with open('graphcompute/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)


if not version:
    raise RuntimeError("Can't find version information")

with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')


setup(
    name='graphcompute',
    version=version,
    description='Aliyun GraphCompute Python SDK',
    long_description=readme,
    install_requires=['gremlinpython>=3.4.2'],
    include_package_data=True,
    url='https://www.aliyun.com/product/graphcompute',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ]
)
