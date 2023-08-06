
#! coding: utf-8
import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='amaraapi',
    version='0.0.6',
    packages=['amaraapi'],
    include_package_data=True,
    keywords='amara api wrapper',
    license='BSD License',
    install_requires=['requests'],
    description='Python Amara API Wrapper',
    long_description=README,
    url='https://github.com/diegoami/amaraapi/',
    author='Diego Amicabile',
    author_email='diego.amicabile@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
)