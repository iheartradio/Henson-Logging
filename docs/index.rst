==============
Henson-Logging
==============

Henson-Logging is a plugin that allows you to easily use structured logging
(via `structlog <http://structlog.readthedocs.io>`_) with a Henson application.

Quickstart
==========

.. code::

    from henson import Application
    from henson_logging import Logging

    app = Application(__name__)
    logger = Logging(app)

In addition to giving you a logger that can be used throughout your
application, it will replace Henson's internal logger with the new one.

Configuration
=============

The following configuration settings can be added to the application's
settings.

+------------------------+----------------------------------------------------+
| ``LOG_FORMAT``         | The :class:`logging.LogRecord` format to use when  |
|                        | logging messages. For most uses the default format |
|                        | is sufficient as all names added to the message    |
|                        | will be included in it. Any additional values      |
|                        | provided through :class:`logging.LogRecord` can    |
|                        | be included in the message through the use of      |
|                        | of processors.                                     |
|                        | default: ``'%(message)s\n'``                       |
+------------------------+----------------------------------------------------+
| ``LOG_FORMATTER``      | The formatter to use in conjunction with the       |
|                        | handler.                                           |
|                        | default: ``'henson'``                              |
+------------------------+----------------------------------------------------+
| ``LOG_HANDLER``        | The log handler to use.                            |
|                        | default: ``'logging.StreamHandler'``               |
+------------------------+----------------------------------------------------+
| ``LOG_HANDLER_KWARGS`` | A dict of kwargs to be passed to the log handler   |
|                        | class's ``__init__`` method.                       |
|                        | default: ``{}``                                    |
+------------------------+----------------------------------------------------+
| ``LOG_LEVEL``          | The threshold of logged messages. Any messages     |
|                        | below this level will be ignored.                  |
|                        | default: ``'INFO'``                                |
+------------------------+----------------------------------------------------+
| ``LOG_CONTEXT_CLASS``  | The type of mapping to use to track field names    |
|                        | included in messages.                              |
|                        | default: ``dict``                                  |
+------------------------+----------------------------------------------------+

.. note::
    There are other configuration settings supported by Henson-Logging but they
    are intended for future and/or advanced uses, and as such have been omitted
    from the section.

Contents:

.. toctree::
   :maxdepth: 1

   api
   changes


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

