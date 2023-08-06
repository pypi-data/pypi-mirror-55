# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 19:22:23 2019

@author: mjaszczykowski
"""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspectrum-MTJ",
    version="1.1.6",
    author="Marcin Jaszczykowski",
    author_email="marcinjaszczykowski@gmail.com",
    description="UV-VIS spectra analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=["pyspectrum"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)