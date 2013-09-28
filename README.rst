======
Bakery
======

.. figure:: https://raw.github.com/muffins-on-dope/bakery/master/docs/source/_static/logo.jpg
   :target: http://thenounproject.com/noun/cookie-jar/#icon-No18366
   :align: right
   :alt: Logo by Nikki Rodriguez

.. image:: https://badge.fury.io/py/bakery.png
    :target: http://badge.fury.io/py/bakery

.. image:: https://travis-ci.org/muffins-on-dope/bakery.png?branch=master
        :target: https://travis-ci.org/muffins-on-dope/bakery

.. image:: https://coveralls.io/repos/muffins-on-dope/bakery/badge.png
        :target: https://coveralls.io/r/muffins-on-dope/bakery

.. image:: https://pypip.in/d/bakery/badge.png
        :target: https://crate.io/packages/bakery?version=latest


Installation
------------

.. code-block:: bash

    $ Create your virtualenv (recommended, use virtualenvwrapper)
    $ virtualenv env

    $ # Clone repository
    $ git clone git@github.com:muffins-on-dope/bakery.git

    $ # Activate Environment and install
    $ source env/bin/activate
    $ pip install -r requirements/development.txt

    $ # run tests
    $ python manage.py test


Edit settings
-------------

Ignore development settings.

.. code-block:: bash

    $ git update-index --assume-unchanged bakery/settings/development.py

This ignores all future changes to your local development settings.

Edit ``bakery/settings/development.py`` and adapt to your environment.


Setup the database
------------------

.. code-block:: bash

    $ python manage.py syncdb --migrate --noinput


Superuser & example data
------------------------

.. code-block:: bash

    $ # Create a new super user
    $ python manage.py createsuperuser
    $ python import.py

Now you can run the webserver and start using the site.

.. code-block::

   $ python manage.py runserver

This starts a local webserver on `localhost:8000 <http://localhost:8000/>`_.

Resources
---------

* `Documentation <https://bakery.readthedocs.org/>`_
* `Bug Tracker <https://github.com/muffins-on-dope/bakery/issues/>`_
* `Code <https://github.com/muffins-on-dope/bakery/>`_
