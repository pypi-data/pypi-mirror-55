#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bottle_oauthproxy",
    version="0.1",
    author="Ahmed El-Sayed",
    author_email="ahmed.m.elsayed93@gmail.com",
    description="oauth2 proxy server, client and authenticator for bottle server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahelsayd/bottle-oauthproxy",
    install_requires=["beaker", "nacl", "requests", "bottle"],
    packages=find_packages(),
)
