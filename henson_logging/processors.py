"""Custom processors."""


def add_logger_name(logger, method_name, event_dict):
    """Add the logger name to the event dict.

    structlog offers a nearly identical processor. The difference is
    that this implementation uses ``"app"`` as the key instead of
    ``"logger"``.
    """
    event_dict['app'] = logger.name
    return event_dict
