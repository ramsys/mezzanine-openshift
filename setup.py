#!/usr/bin/env python

from setuptools import setup

setup(
    name='mezzanine-openshift',
    version='1.2',
    description='Mezzanine configured for deployment on OpenShift.',
    author='Isaac Bythewood',
    author_email='isaac@bythewood.me',
    url='http://isaacbythewood.com/',
    install_requires=[
        'Django==1.6.4',
        'mezzanine==3.1.3',
        'django_compressor==1.3'
    ],
)
