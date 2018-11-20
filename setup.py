#!/usr/bin/env python

from setuptools import setup, find_packages

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
        version='0.0.7',
        entry_points={
            'console_scripts': [
                'pyrrot = pyrrot:main'
            ]
        },
        install_requires=['requests', 'packaging']
    )
