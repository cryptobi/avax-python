#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest>=3'
]

setup(
    author="Alex Willmer",
    author_email='alex@moreati.org.uk',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Reference implementation of CB58 encoding used by AVA",
    #entry_points={
    #    'console_scripts': [
    #        'cb58ref=cb58ref.cli:main',
    #    ],
    #},
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cb58 base58 ava',
    name='cb58ref',
    packages=find_packages(include=['cb58ref', 'cb58ref.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/moreati/cb58ref',
    version='0.2.0',
    zip_safe=True,
)
