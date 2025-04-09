from setuptools import setup, find_packages

setup(
    name="myapp",
    version="0.1",
    packages=find_packages(exclude=["myapp.tests", "myapp.tests.*"]),  # Automatically finds the myapp package.
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "myapp=myapp.cli:main",  # This creates a command 'myapp' to run your CLI.
        ],
    },
)
