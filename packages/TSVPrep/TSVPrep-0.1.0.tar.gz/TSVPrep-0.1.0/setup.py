"""
Pypi Setup
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TSVPrep",
    version="0.1.0",
    author="Brian Monaccio",
    author_email="brianmonaccio@gmail.com",
    description="Module for locating and proofreading .tsv files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/learnsometing/TSVPrep",
    packages=setuptools.find_packages(exclude=["tests", "data"]),
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
)
