# -*- coding: utf-8 -*-
"""
@author: He Dekun
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "hdk_pkg_critest", # Replace with your own username
    version = "1.0.0",
    author = "He Dekun",
    author_email = "hede0001@e.ntu.edu.sg",
    description = "A small example package for CRI PMT test.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/HDKidd/hdk-pkg-critest",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)