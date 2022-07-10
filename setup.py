from setuptools import find_packages, setup
from package import Package

setup(
    author="FatherAnarchy",
    author_email="fatheranarchy@programmer.com",
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        "package": Package
    }
)