from setuptools import find_packages, setup

setup(
    name='Henson-Logging',
    version='0.2.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Henson>=0.2.0',
        'structlog==15.1.0',
    ],
    tests_require=[
        'tox',
    ],
)
