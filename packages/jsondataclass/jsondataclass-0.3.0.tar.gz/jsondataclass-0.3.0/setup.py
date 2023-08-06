#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    name="jsondataclass",
    version="0.3.0",
    description="Json dataclass mapper",
    long_description=readme + "\n\n" + history,
    author="Aleksey Shulga",
    author_email="oleksii.shulga@gmail.com",
    url="https://github.com/tushkanin/jsondataclass",
    packages=["jsondataclass"],
    package_dir={"jsondataclass": "jsondataclass"},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=requirements,
    setup_requires=setup_requirements,
    license="MIT license",
    zip_safe=False,
    keywords="jsondataclass dataclasses json",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
