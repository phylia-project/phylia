
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="phylia",
    version="0.0.1",
    description="phylia is a python package for phytosociological information analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phylia-project/phylia.git",
    author="Thomas de Meij",
    author_email="mailphylia@gmail.com",
    license="GNU3.0",
    packages=["phylia"],
    install_requires=[
        'pandas','numpy','geopandas','fiona','pyodbc',
        ],
    include_package_data=True,
    package_data={'': ['data/*.csv']},
)
