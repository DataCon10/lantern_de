from setuptools import setup, find_packages

setup(
    name="myapp",
    version="0.1",
    packages=find_packages(exclude=["myapp.tests", "myapp.tests.*"]),
    install_requires=[
        "requests",
    ],
)
