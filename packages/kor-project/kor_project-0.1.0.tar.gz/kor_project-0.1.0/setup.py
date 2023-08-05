from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kor_project',
    version='0.1.0',
    description="Use this package to work with kor files",
    py_modules=["kor"],
    package_dir={'': 'src'},
    classifiers= [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"],

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/KoraKu/Kor_Project",
    author="Hugo Costa",
    author_email="costhug@orange.fr",

    )
