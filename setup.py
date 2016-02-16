from setuptools import find_packages, setup

setup(
    name='Henson-Logging',
    version='0.3.0',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Henson>=0.2.0',
        'structlog',
    ],
    tests_require=[
        'tox',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ]
)
