
from setuptools import find_packages, setup

setup(
    name='papersample',
    version='0.0.1',
    description='샘플패키지',
    long_description=open('README.md').read(),
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)