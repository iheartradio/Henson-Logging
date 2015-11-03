==============
Henson-Logging
==============

Henson-Logging is a plugin that allows you to easily use structured logging
(via `structlog <http://structlog.rtfd.org>`_) with a Henson application.

Quickstart
==========

.. code::

    from henson import Application
    from henson_logging import Logging

    logger = Logging()
    app = Application(__name__, logger=logger)
    logger.init_app(app)

.. todo:: Fix this API. It's awkward.

Configuration
=============

The following configuration settings can be added to the application's
settings.

===================== =========================================================
``LOG_FORMAT``        The :class:`logging.LogRecord` format to use when
                      logging messages. For most uses the default format is
                      sufficient as all names added to the message will be
                      included in it. Any additional values provided through
                      :class:`logging.LogRecord` can be included in the message
                      through the use of processors.
                      default: ``'%(message)s\n'``
``LOG_HANDLER``       The log handler to use.
                      default: ``'logging.StreamHandler'``
``LOG_LEVEL``         The threshold of logged messages. Any messages below this
                      level will be ignored.
                      default: ``'INFO'``
``LOG_CONTEXT_CLASS`` The type of mapping to use to track field names included
                      in messages.
                      default: ``dict``
===================== =========================================================

.. note::
    There are other configuration settings supported by Henson-Logging but they
    are intended for future and/or advanced uses, and as such have been omitted
    from the section.

Contents:

.. toctree::
   :maxdepth: 1

   changes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

