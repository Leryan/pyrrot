#!/usr/bin/env python

import os

from setuptools import setup, find_packages

VERSION = os.getenv('VERSION', '0.0.1')

def requirements():
    pkgpath = os.path.dirname(os.path.realpath(__file__))
    reqs = []
    requires_path = os.path.join(pkgpath, 'requirements.txt')

    with open(requires_path) as f:
        reqs = f.readlines()

    reqs = filter(None, [r.strip() for r in reqs])
    reqs = [r for r in reqs if not r.startswith('#')]

    return reqs

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
        },
        install_requires=requirements()
    )
