#!/usr/bin/env python
import os
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because setuptools doesn't have
# an easy way to do this. Taken from Django.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
django_dir = 'bakery'

for dirpath, dirnames, filenames in os.walk(django_dir):
    # Ignore PEP 3147 cache dirs and those whose names start with '.'
    dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__']
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup(
    name='bakery',
    version='0.1a0',
    description='cookiecutter index project -- DjangoDash 2013',
    long_description=read('README.rst'),
    author='Christopher Grebs, Markus Holtermann',
    author_email='cg@webshox.org, info@markusholtermann.eu',
    url='https://github.com/muffins-on-dope/bakery',
    license='BSD',
    packages=find_packages(exclude=["tests"]),
    data_files=data_files,
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
