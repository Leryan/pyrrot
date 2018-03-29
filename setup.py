#!/usr/bin/env python

import os

from setuptools import setup, find_packages

VERSION = os.getenv('VERSION', '0.0.1')

if __name__ == '__main__':
    setup(
        name='pyrrot',
        author='Florent Peterschmitt',
        author_email='florent@peterschmitt.fr',
        description='Check for rotten python requirements',
        license='MIT',
        zip_safe=True,
        url='https://github.com/Leryan/pyrrot',
        packages=find_packages(exclude=['test.*']),
        version=VERSION,
        entry_points={
            'console_scripts': [
                'pyrrot = pyrrot:main'
            ]
        }
    )
