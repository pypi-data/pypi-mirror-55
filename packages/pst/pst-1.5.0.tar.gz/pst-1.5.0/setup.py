#!/usr/bin/env python

from setuptools import setup

exec(open("pst/info.py").read())

setup(
    name="pst",
    author="mixed.connections",
    author_email="mixed.connections2@gmail.com",
    description="A reproduction of pstree",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="https://github.com/mixedconnections/pst",
    packages=["pst"],
    data_files=[("/usr/local/bin",["bin/pst"])],
    use_incremental=True,
    setup_requires=['incremental'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Utilities",
    ],
    keywords = "shell pstree",
    license = "MIT"
)
