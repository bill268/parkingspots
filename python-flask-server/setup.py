# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="a street parking spot reservation service",
    author_email="bill.hongwu.chen@gmail.com",
    url="",
    keywords=["Swagger", "a street parking spot reservation service"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Assume that we are building a street parking spot reservation service. Users should be able to view street parking spots, reserve and pay for the parking spots or cancel their reservations. 
    """
)

