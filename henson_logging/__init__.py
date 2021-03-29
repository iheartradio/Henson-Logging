"""Logging plugin for Henson."""

import logging
import logging.config
import os
import pkg_resources

from henson import Extension
import structlog

from . import processors

__all__ = ('Logging',)

try:
    _dist = pkg_resources.get_distribution(__package__)
    if not __file__.startswith(os.path.join(_dist.location, __package__)):
        # Manually raise the exception if there is a distribution but
        # it's installed from elsewhere.
        raise pkg_resources.DistributionNotFound
except pkg_resources.DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version


class Logging(Extension):
    """An interface to use structured logging.

    Args:
        app (~typing.Optional[henson.base.Application]): An application
            instance that has an attribute named settings that contains
            a mapping of settings to configure logging.
    """

    DEFAULT_SETTINGS = {
        'LOG_DATE_FORMAT': None,
        'LOG_FORMAT': '%(message)s\n',
        'LOG_FORMATTER': 'henson',
        'LOG_HANDLER': 'logging.StreamHandler',
        'LOG_HANDLER_KWARGS': {},
        'LOG_LEVEL': 'DEBUG',
        'LOG_VERSION': 1,

        # TODO: The format for TimeStamper should be controllable
        # through the application settings. Right now the
        # LOG_DATE_FORMAT setting is ignored.
        'LOG_PROCESSORS': (
            structlog.stdlib.filter_by_level,
            processors.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ),

        'LOG_CONTEXT_CLASS': dict,
        'LOG_FACTORY': structlog.stdlib.LoggerFactory(),
        'LOG_WRAPPER_CLASS': structlog.stdlib.BoundLogger,
        'LOG_PROPAGATE': True,
    }

    def __init__(self, app=None):
        """Initialize the instance."""
        super().__init__(app)

        self._logger = None

    def init_app(self, app):
        """Initialize the application and register a logger.

        Args:
            app (henson.base.Application): The application to
                initialize.
        """
        super().init_app(app)
        # the lines defining log levels (critical, debug, etc)
        # use the state of Henson base logger's (app.logger).
        # In order to prevent the current henson_logging.Logger
        # object from passing its log events to the Henson base
        # logger's handler when invoking functions set in those lines,
        # propagate must be false.
        app.logger.propagate = app.settings['LOG_PROPAGATE']
        app.logger = self

    # the invocation of these lambda functions rely on the state
    # of s.logger (henson.base.Logger)
    # at the time of variable setting
    critical = lambda s, *a, **kw: s.logger.critical(*a, **kw)
    debug = lambda s, *a, **kw: s.logger.debug(*a, **kw)
    error = lambda s, *a, **kw: s.logger.error(*a, **kw)
    info = lambda s, *a, **kw: s.logger.info(*a, **kw)
    exception = lambda s, *a, **kw: s.logger.exception(*a, **kw)
    fatal = lambda s, *a, **kw: s.logger.fatal(*a, **kw)
    log = lambda s, *a, **kw: s.logger.log(*a, **kw)
    setLevel = lambda s, l: s.logger.setLevel(l)  # NOQA: N815
    warning = lambda s, *a, **kw: s.logger.warning(*a, **kw)

    def get_effective_level(self):
        """Return the effective level for the logger.

        Returns:
            int: The effective level.

        .. versionadded:: 0.4

        """
        return self.logger.getEffectiveLevel()

    getEffectiveLevel = get_effective_level  # NOQA: N815
    """An alias for :meth:`get_effective_level` provided for
    compatibility with :meth:`logging.Logger.getEffectiveLevel`.
    """

    @property
    def logger(self):
        """Return the logger.

        Returns:
            logging.RootLogger: The logger.

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
                        **self.app.settings['LOG_HANDLER_KWARGS'],
                        'class': self.app.settings['LOG_HANDLER'],
                        'formatter': self.app.settings['LOG_FORMATTER'],
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

            self._logger = structlog.get_logger(self.app.name).bind()

        return self._logger

    def set_level(self, level):
        """Set the logging level for the logger.

        Args:
            level (~typing.Union[int, str]): The logging level to set.
                If the value is a ``str``, it must be a valid level
                defined in :mod:`logging`.

        .. versionadded:: 0.4
        """
        self.logger.setLevel(level)

    setLevel = set_level  # NOQA: N815
    """An alias for :meth:`set_level` provided for compatibility with
    :meth:`logging.Logger.setLevel`.
    """
