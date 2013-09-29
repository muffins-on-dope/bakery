#-*- coding: utf-8 -*-
from bakery.cookies.models import Cookie


repos = [
    'https://github.com/audreyr/cookiecutter-pypackage',
    'https://github.com/sloria/cookiecutter-flask',
    'https://github.com/lucuma/cookiecutter-flask-env',
    'https://github.com/marcofucci/cookiecutter-simple-django',
    'https://github.com/pydanny/cookiecutter-django',
    'https://github.com/pydanny/cookiecutter-djangopackage',
    'https://github.com/openstack-dev/cookiecutter',
    'https://github.com/sloria/cookiecutter-docopt',
    'https://github.com/vincentbernat/bootstrap.c',
    'https://github.com/audreyr/cookiecutter-jquery',
    'https://github.com/audreyr/cookiecutter-component',
    'https://github.com/larsyencken/pandoc-talk',
    'https://github.com/audreyr/cookiecutter-complexity',
]


for repo in repos:
    print('Importing {0}'.format(repo))
    Cookie.objects.import_from_url(repo)
    print('Imported {0}'.format(repo))
    print()
