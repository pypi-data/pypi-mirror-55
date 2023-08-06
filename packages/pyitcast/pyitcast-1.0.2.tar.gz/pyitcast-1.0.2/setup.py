# -*- coding: utf-8 -*-
#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='pyitcast',
    version='1.0.2',
    description='传智播客开源分享工具包!',
    url='https://github.com/StephenZMZ/OneLine.git',
    author='Stephen.Z',
    author_email='15242200221@163.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python itcast',
    packages = find_packages(exclude = ['MANIFEST.in']),
    include_packages_data = True
    )   
