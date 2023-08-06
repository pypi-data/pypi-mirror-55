#!/usr/bin/env python
from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ufoLib2",
    use_scm_version={"write_to": "src/ufoLib2/_version.py"},
    description="ufoLib2 is a UFO font library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adrien Tétar",
    author_email="adri-from-59@hotmail.fr",
    url="https://github.com/adrientetar/ufoLib2",
    license="Apache 2.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["fonttools[ufo] >= 3.34.0", "attrs >= 18.2.0"],
    setup_requires=["setuptools_scm"],
    extras_require={"lxml": ["lxml"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: Fonts",
        "License :: OSI Approved :: Apache Software License",
    ],
)
