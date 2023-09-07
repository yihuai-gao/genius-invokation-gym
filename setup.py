import os
from distutils.core import setup

from setuptools import find_packages

_package_name = "gisim"

here = os.path.abspath(os.path.dirname(__file__))


def _load_req(file: str):
    with open(file, "r", "utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


setup(
    # information
    name="genius-invokation-gym",
    version="0.1.0",
    packages=find_packages(include=(_package_name, "%s.*" % _package_name)),
    package_data={
        package_name: ["*.yaml", "*.yml"]
        for package_name in find_packages(include=("*"))
    },
    description="A gym environment for the Genshin Genius Invokation game.",
    long_description_content_type="text/markdown",
    author="Genius Invokation Gym Contributors",
    author_email="any@example.com",
    license="Apache License, Version 2.0",
    keywords="genshin",
    # environment
    python_requires=">=3.7",
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
