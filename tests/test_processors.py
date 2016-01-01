"""Test the custom processors."""

from henson_logging import processors


def test_add_logger_name(test_logger):
    """Test add_logger_name."""
    actual = processors.add_logger_name(test_logger, '', {})
    assert actual['app'] == test_logger.name
