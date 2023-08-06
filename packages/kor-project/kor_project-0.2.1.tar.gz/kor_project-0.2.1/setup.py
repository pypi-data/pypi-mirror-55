from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kor_project',
    version='0.2.1',
    description="Use this package to work with kor files",
    py_modules=["kor"],
    packages=find_packages(),
    classifiers= [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"],

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/KoraKu/Kor_Project",
    author="Hugo Costa",
    author_email="costhug@orange.fr",

    )
