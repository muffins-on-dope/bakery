#!/usr/bin/env python
import os
import codecs
from setuptools import setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def fullsplit(path, result=None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
src_dir = 'bakery'

for dirpath, dirnames, filenames in os.walk(src_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    for filename in filenames:
        if filename.endswith('.py'):
            packages.append('.'.join(fullsplit(dirpath)))
        else:
            data_files.append(
                [dirpath, [os.path.join(dirpath, f) for f in filenames]],
            )


setup(
    name='bakery',
    version='0.1a0',
    description='cookiecutter index project -- DjangoDash 2013',
    long_description=read('README.rst'),
    author='Christopher Grebs, Markus Holtermann',
    author_email='cg@webshox.org, info@markusholtermann.eu',
    url='https://github.com/muffins-on-dope/bakery',
    license='BSD',
    packages=[
        'bakery',
        'bakery.cookies',
    ],
    install_requires=[
        'Django==1.5.4',
        'PyGithub==1.19.0',
        'South',
        'jsonfield>=0.9.19',
        'python-social-auth>=0.1.13',
    ],
    data_files=data_files,
    include_package_data=False,
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
    zip_safe=False
)
