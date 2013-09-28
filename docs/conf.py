# -*- coding: utf-8 -*-
import os
import sys

import pkg_resources

sys.path.append(os.path.abspath('_themes'))
sys.path.append(os.path.abspath('.'))


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx',
              'sphinx.ext.doctest', 'sphinx.ext.todo']

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'bakery'
copyright = u'2013, muffins on dope'

try:
    distribution = pkg_resources.get_distribution('bakery')
    version = release = distribution.version
except pkg_resources.DistributionNotFound:
    version = release = 'unknown'

exclude_patterns = []

html_theme_path = ['_themes']
html_theme = 'flask'

html_static_path = ['_static']

htmlhelp_basename = 'bakerydoc'

latex_elements = {
}

latex_documents = [
    ('index', 'Bakery.tex', u'Bakery Documentation',
     u'Muffins on Dope', 'manual'),
]
man_pages = [
    ('index', 'bakery', u'Bakery Documentation',
     [u'Muffins on Dope'], 1)
]

texinfo_documents = [
    ('index', 'Bakery', u'Bakery Documentation',
     u'Muffins on Dope', 'Bakery', '',
     'Miscellaneous'),
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/2.7', None),
    'cookiecutter': ('https://cookiecutter.readthedocs.org/en/latest/', None),
}

# Python's docs don't change every week.
intersphinx_cache_limit = 90  # days

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if on_rtd:
    html_theme = 'default'

pygments_style = 'flask_theme_support.FlaskyStyle'
