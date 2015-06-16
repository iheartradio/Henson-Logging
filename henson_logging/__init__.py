"""Logging plugin for Henson."""

import logging
import logging.config

import structlog

from . import processors

__all__ = ('Logging',)


class Logging:

    """An interface to use structured logging.

    Args:
        app (:class:`~henson.Application`, optional): An application
          instance that has an attribute named settings that contains a
          mapping of settings to configure logging.
    """

    def __init__(self, app=None):
        """Initialize the instance."""
        self._app = None
        self._logger = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize an application for structured logging.

        Args:
            app (:class:`~henson.Application`): An application instance
              that has an attribute named settings that contains a
              mapping of settings to configure logging.
        """
        app.settings.setdefault('LOG_DATE_FORMAT', None)
        app.settings.setdefault('LOG_FORMAT', '%(message)s\n')
        app.settings.setdefault('LOG_HANDLER', 'logging.StreamHandler')
        app.settings.setdefault('LOG_LEVEL', 'DEBUG')
        app.settings.setdefault('LOG_VERSION', 1)

        # TODO: The format for TimeStamper should be controllable
        # through the application settings. Right now the
        # LOG_DATE_FORMAT setting is ignored.
        app.settings.setdefault('LOG_PROCESSORS', (
            structlog.stdlib.filter_by_level,
            processors.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ))
        app.settings.setdefault('LOG_CONTEXT_CLASS', dict)
        app.settings.setdefault(
            'LOG_FACTORY', structlog.stdlib.LoggerFactory())
        app.settings.setdefault(
            'LOG_WRAPPER_CLASS', structlog.stdlib.BoundLogger)

        self._app = app

    @property
    def app(self):
        """Return the registered app."""
        if not self._app:
            raise RuntimeError(
                'No application has been assigned to this instance. '
                'init_app must be called before referencing instance.app.')
        return self._app

    critical = lambda s, *a, **kw: s.logger.critical(*a, **kw)
    debug = lambda s, *a, **kw: s.logger.debug(*a, **kw)
    error = lambda s, *a, **kw: s.logger.error(*a, **kw)
    info = lambda s, *a, **kw: s.logger.info(*a, **kw)
    exception = lambda s, *a, **kw: s.logger.exception(*a, **kw)
    fatal = lambda s, *a, **kw: s.logger.fatal(*a, **kw)
    log = lambda s, *a, **kw: s.logger.log(*a, **kw)
    warning = lambda s, *a, **kw: s.logger.warning(*a, **kw)

    @property
    def logger(self):
        """Return the logger.

        Returns:
            :class:`~logging.RootLogger`: The logger.
        """
        if not self._logger:

            settings = {
                'version': self.app.settings['LOG_VERSION'],
                'formatters': {
                    'henson': {
                        'format': self.app.settings['LOG_FORMAT'],
                        'datefmt': self.app.settings['LOG_DATE_FORMAT'],
                    },
                },
                'handlers': {
                    'henson': {
                        'class': self.app.settings['LOG_HANDLER'],
                        'formatter': 'henson',
                    },
                },
                'loggers': {
                    self.app.name: {
                        'handlers': ['henson'],
                        'level': self.app.settings['LOG_LEVEL'],
                    },
                }
            }

            logging.config.dictConfig(settings)

            structlog.configure(
                processors=self.app.settings['LOG_PROCESSORS'],
                context_class=self.app.settings['LOG_CONTEXT_CLASS'],
                logger_factory=self.app.settings['LOG_FACTORY'],
                wrapper_class=self.app.settings['LOG_WRAPPER_CLASS'],
                cache_logger_on_first_use=True,
            )

            self._logger = structlog.get_logger(self.app.name)

        return self._logger
