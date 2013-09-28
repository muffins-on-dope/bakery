#!/usr/bin/env python
import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='bakery',
    version='0.1a0',
    description='cookiecutter index project -- DjangoDash 2013',
    long_description=read('README.rst'),
    author='Christopher Grebs, Markus Holtermann',
    author_email='cg@webshox.org, info@markusholtermann.eu',
    url='https://github.com/muffins-on-dope/bakery',
    license='BSD',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'Django==1.5.4',
        'PyGithub==1.19.0',
        'South',
        'jsonfield>=0.9.19',
        'python-social-auth>=0.1.13',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Framework :: Django',
    ],
    zip_safe=False,
    include_package_data=True
)
