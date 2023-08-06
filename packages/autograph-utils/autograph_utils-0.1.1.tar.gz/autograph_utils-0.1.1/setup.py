#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "aiohttp>=3.6", "cryptography>=2.8", "ecdsa>=0.13"]

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Ethan Glasser-Camp",
    author_email="eglassercamp@mozilla.com",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="A library to simplify use of Autograph",
    entry_points={"console_scripts": ["autograph_utils=autograph_utils.cli:main"]},
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="autograph_utils",
    name="autograph_utils",
    packages=find_packages(include=["autograph_utils", "autograph_utils.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/mozilla-services/python_autograph_utils",
    version="0.1.1",
    zip_safe=False,
)
