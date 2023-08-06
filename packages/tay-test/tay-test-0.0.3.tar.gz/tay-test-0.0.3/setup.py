#!/usr/bin/env python
# -*- coding:utf-8 -*-


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tay-test",  # Replace with your own username
    version="0.0.3",
    author="古寒飞",
    author_email="tay3223@qq.com",
    description="Tay的一个简单测试",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/tay3223/tmp.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
