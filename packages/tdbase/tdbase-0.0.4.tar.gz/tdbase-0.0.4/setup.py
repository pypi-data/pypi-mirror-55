#!/usr/bin/python3

import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

#open("tdbase/version","rt").read()
import tdbase

setuptools.setup(
    name="tdbase",
    version=tdbase.__version__,
    author="Jesper Ribbe",
#    author_email="author@example.com",
    description="Text based database package",
    long_description=long_description,
    long_description_content_type="text/markdown",
#    url="https://github.com/pypa/sampleproject",
#    packages=setuptools.find_packages(),
    packages=["tdbase"],
    package_data={"tdbase":["py.typed"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
)

