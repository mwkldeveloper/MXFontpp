#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# 讀取 README 檔案
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 讀取 requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mxfontpp",
    version="0.0.1",
    author="NAVER Corp.",
    author_email="",
    description="MX-Font++: A Multi-Expert Font Generation System",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/clovaai/mxfontpp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.json", "*.txt", "*.ttf"],
    },
    zip_safe=False,
    keywords="font generation, deep learning, pytorch, multi-expert, typography",
    project_urls={
        "Bug Reports": "https://github.com/clovaai/mxfontpp/issues",
        "Source": "https://github.com/clovaai/mxfontpp",
        "Documentation": "https://github.com/clovaai/mxfontpp#readme",
    },
)
