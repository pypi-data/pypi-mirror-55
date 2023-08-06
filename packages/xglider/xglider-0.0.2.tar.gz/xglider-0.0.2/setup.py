#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from codecs import open

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()

with open('requirements.txt', encoding='utf-8') as f:
    requirements = f.read()

#def test_requirements():
#    with open('test_requirements.txt', encoding='utf-8') as f:
#        requirements = f.read()
#    return requirements

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    name='xglider',
    version='0.0.2',
    author="Guilherme Castelão",
    author_email='castelao@ucsd.edu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Generic tools to handle underwater gliders' data",
    entry_points={
        'console_scripts': [
            'xglider=xglider.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='underwater glider oceanography',
    packages=find_packages(include=['xglider']),
    setup_requires=setup_requirements,
    test_suite='tests',
    # tests_require=test_requirements(),
    url='https://github.com/castelao/xglider',
    project_urls={
        "Documentation": "https://xglider.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/castelao/xglider",
    },
    zip_safe=False,
    extras_require={
        # 'test': requirements_test,
        'cmocean': ["cmocean>=2.0"],
        'plot': ["matplotlib>=3.0.0"]
        }
)
