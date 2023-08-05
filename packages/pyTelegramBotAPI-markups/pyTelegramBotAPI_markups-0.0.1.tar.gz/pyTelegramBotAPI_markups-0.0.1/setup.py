#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    name='pyTelegramBotAPI_markups',
    version='0.0.1',
    description="Handy markups for pyTelegramBotApi",
    long_description=readme,
    author="Dmitry Makarov",
    author_email='mit.makaroff@gmail.com',
    url='',
    packages=[
        'markups',
    ],
    package_dir={
        'markups': 'markups',
    },
    include_package_data=True,
    download_url="https://github.com/Mityuha/pyTelegramBotAPI_markups/archive/0.0.1.tar.gz",
    install_requires=[
        'pyTelegramBotAPI',
        "trafaret_config"
    ],
    license="",
    zip_safe=False,
    keywords='markups',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
