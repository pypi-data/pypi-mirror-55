===================================
Kleides Multi Factor Authentication
===================================


.. image:: https://img.shields.io/pypi/v/kleides_mfa.svg
        :target: https://pypi.python.org/pypi/kleides_mfa

.. image:: https://img.shields.io/travis/Urth/kleides_mfa.svg
        :target: https://travis-ci.org/Urth/kleides_mfa

.. image:: https://readthedocs.org/projects/kleides-mfa/badge/?version=latest
        :target: https://kleides-mfa.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Interface components to configure and manage multi factor authentication


* Free software: GNU General Public License v3
* Documentation: https://kleides-mfa.readthedocs.io.

Install
-------

.. code-block::

   pip install kleides-mfa


.. code-block::

   MIDDLEWARE = [
       ...
       'django.contrib.auth.middleware.AuthenticationMiddleware',
       'kleides_mfa.middleware.KleidesAuthenticationMiddleware',
       ...
   ]
