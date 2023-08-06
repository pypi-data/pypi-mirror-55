# -*- coding:utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nsf_utils",
    version="0.0.1",
    author="ethan.su",
    author_email="su930116@gmail.com",
    description="some common tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ethan-su/nsf-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
