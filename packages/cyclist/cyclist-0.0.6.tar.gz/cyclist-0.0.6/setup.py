from setuptools import find_packages
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cyclist",
    version="0.0.6",
    author="Ben Andrews",
    author_email="mortimermcmiresa@gmail.com",
    description="Cycle-based data analysis toolbox",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MortimerMcMire/cyclist",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[
	'pandas>=0.11.0'
	],
)