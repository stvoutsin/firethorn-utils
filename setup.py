import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "firethorn-utils",
    version = "0.1.0",
    author = "Stelios Voutsinas",
    author_email = "stv@roe.ac.uk",
    description = ("A python suite for utility functions for firethorn"),
    license = "BSD",
    keywords = "firethorn vo",
    url = "http://wfau.metagrid.co.uk/code/firethorn",
    include_package_data = True,  
    packages=['firethorn_utils'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Utilities",
        "License :: GPL License",
    ],
    install_requires=[
        'numpy>=1.4.0',
        'astropy>=0.4.1',
        'pyodbc>=4.0.21',
        'pyparsing>=2.2.0',
        'pycurl>=7.43.0'
    ]
)

