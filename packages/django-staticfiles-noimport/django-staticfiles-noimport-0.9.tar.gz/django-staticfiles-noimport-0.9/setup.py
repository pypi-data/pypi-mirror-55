#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django-staticfiles-noimport",
    version="0.9",
    author="Philip Kimmey",
    author_email="philip+pypi@rover.com",
    description="Allows Django staticfiles commands to be run without importing all apps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roverdotcom/django-staticfiles-noimport",
    packages=["staticfiles_noimport"],
    scripts=["bin/collectstatic", "bin/findstatic"],
    install_requires=["Django>=1.11"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: Django",
    ],
    python_requires=">=3.6",
)
