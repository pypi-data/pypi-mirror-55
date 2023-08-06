# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pytdd',
    version='1.1.0',
    description='python TDD assistant, runs test command on source file change only',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Alex Chauvin',
    author_email='ach@meta-x.org',
    url='https://gitlab.com/achauvinhameau/pytdd',
    # license=license,
    packages=['pytdd'],

    entry_points={
        'console_scripts': [
            'pytdd = pytdd:main',
        ],
    },

    python_requires='>=3',
    install_requires=['watchdog'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
    ],
)
