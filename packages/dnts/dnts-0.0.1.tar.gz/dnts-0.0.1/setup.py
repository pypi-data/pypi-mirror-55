from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dnts',
    version='0.0.1',
    author='Neil C. Obremski',
    author_email='neilo@donuts.email',
    packages=find_packages(),
    url='https://github.com/neilodonuts/dnts',
    description='Domain Names, Tools & Stuff',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
