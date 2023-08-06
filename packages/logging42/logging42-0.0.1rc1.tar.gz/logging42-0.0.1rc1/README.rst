logging42
=========

A configuration for the loguru (https://github.com/Delgan/loguru) logger.

It is important that it be the first import to run the standard logging basicConfig method.

Features
--------

- Stderr output

- intercepted logging from client libraries

- Disabled better exceptions for log levels above debug to mitgate secret leaking

Installation
------------

.. code:: bash

   pip install logging42


Examples
--------

**main.py**

.. code:: python

    from logging42 import logger

    logger.debug('hello world)
