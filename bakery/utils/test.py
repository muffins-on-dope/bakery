# -*- coding: utf-8 -*-

from os.path import dirname, join


def read(base, *paths):
    fp = join(dirname(base), *paths)
    with open(fp, 'r') as f:
        return f.read()
