=======
cb58ref
=======

.. image:: https://img.shields.io/pypi/v/cb58ref.svg
        :target: https://pypi.python.org/pypi/cb58ref

.. image:: https://img.shields.io/travis/moreati/cb58ref.svg
        :target: https://travis-ci.com/moreati/cb58ref

.. image:: https://readthedocs.org/projects/cb58ref/badge/?version=latest
        :target: https://cb58ref.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/moreati/cb58ref/shield.svg
     :target: https://pyup.io/repos/github/moreati/cb58ref/
     :alt: Updates

cb58ref is a reference implementation of the CB58 encoding used by `AVA`_.
CB58 is similar to the `Base58Check`_ encoding used in Bitcoin

* both can encode arbitrary an arbitrary byte sequence
* both use the same alphabet
* both append a 4 byte checksum

they differ in the following respects

* CB58 uses the final 4 bytes of ``SHA256(msg)`` as the checksum.
  Base58Check uses the first 4 bytes of ``SHA256(SHA256(msg))`` as the
  checksum.

Usage
-----

.. code:: python

    >>> import cb58ref
    >>> cb58ref.cb58encode(b"Hello world"):
    '32UWxgjUJd9s6Kyvxjj1u'
    >>> cb58ref.cb58decode('32UWxgjUJd9s6Kyvxjj1u')
    b"Hello world"

.. code::

    $ printf "Hello world" | python3 -m cb58ref
    32UWxgjUJd9s6Kyvxjj1u

    $ printf "32UWxgjUJd9s6Kyvxjj1u" | python3 -m cb58ref -d
    Hello world

Installation
------------

.. code::

    $ python3 -m pip install cb58ref

License
-------

* Free software: MIT license

Credits
-------

This package was created with `Cookiecutter`_ and the `audreyr/cookiecutter-pypackage`_ project template.
The ``b58decode()``, and ``b58encode()`` functions are from `base58.py`_, part of Bitcoin Core.

.. _`AVA`: https://www.avalabs.org/
.. _`Base58Check`: https://en.bitcoin.it/wiki/Base58Check_encoding
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`base58.py`: https://github.com/bitcoin/bitcoin/blob/master/contrib/testgen/base58.py
.. _`Bitcoin Core`: https://github.com/bitcoin/bitcoin
