#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ['pytest-runner', 'setuptools']

test_requirements = ['pytest', 'Faker']

setup(
    author="Jonathan López",
    author_email='jlopez@fipasoft.com.mx',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A package description.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kakeibox_controllers',
    name='kakeibox-controllers',
    packages=['kakeibox_controllers',
              'kakeibox_controllers.handlers',
              'kakeibox_controllers.controllers',
              'kakeibox_controllers.controllers.transaction_category',
              'kakeibox_controllers.controllers.transaction_subcategory', ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/kakeibox/kakeibox-cli-app/kakeibox-controllers',
    version='0.9.2',
    zip_safe=False,
)
