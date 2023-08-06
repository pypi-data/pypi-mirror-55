"""
iselenium (innovata selenium)

Revised Date : 2019-11-14
"""
import setuptools


with open("README.md", "r") as f:
    long_description = f.read()
    f.close()

setuptools.setup(
    name="iselenium",
    version="0.0.1",
    author="innovata Sambong",
    author_email="iinnovata@gmail.com",
    description=__doc__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/innovata/iselenium",
    packages=setuptools.find_packages(exclude=["*.jupyter", "*.jupyter.*", "jupyter.*", "jupyter"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
