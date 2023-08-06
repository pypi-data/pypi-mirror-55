# -*- coding: utf-8 -*-
import os
import setuptools
from distutils.core import setup


def read_file_into_string(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ""


def get_readme():
    if os.path.exists("README.md"):
        return read_file_into_string("README.md")
    return ""


setup(
    name="elio-liar",
    packages=["liar", "liar.tests", "liar.model", "liar.raw"],
    install_requires=["python-dateutil", "python-slugify"],
    include_package_data=True,
    version="1.0",
    description="A source of random but realistic looking data the elioWay.",
    author="Tim Bushell",
    author_email="tcbushell@gmail.com",
    url="https://elioway.gitlab.io/elioangels/liar",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing :: Mocking",
    ],
    long_description=get_readme(),
    long_description_content_type="text/markdown",
)
