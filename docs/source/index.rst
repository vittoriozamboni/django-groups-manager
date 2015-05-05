.. Django Groups Manager documentation master file, created by
   sphinx-quickstart on Tue Oct 28 13:53:01 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Django Groups Manager
=====================

Django Groups Manager allows to manage groups based on `django-mptt <https://github.com/django-mptt/django-mptt>`_.

The application offers three main classes: `Group`, `Member` and `GroupMember`.
It's possible to *map* groups and members with Django's auth models, in order to use external applcations such `django-guardian <https://github.com/lukaszb/django-guardian>`_ to handle permissions.

The basic idea of Groups is that each `Group` instance could have a `Group` instance as parent (this relation is managed via django-mptt).

The code is hosted on `github <https://github.com/vittoriozamboni/django-groups-manager>`_.

Documentation
=============

.. toctree::
   :maxdepth: 3

   intro
   auth_integration
   settings
   use_cases
   API 
   tests
   todo
   changelog

.. include:: changelog.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

