from setuptools import setup, find_packages

setup(
    name='powerstrip',
    version='0.0.1',
    description='A Python package to control the SuperviZ power strip',
    packages=find_packages(),
    install_requires=[
        'pyserial',
    ],
)