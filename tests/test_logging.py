"""Test Henson-Logging."""

import logging

import pytest

from henson_logging import Logging


@pytest.mark.parametrize('level', (logging.DEBUG, logging.INFO))
def test_get_effective_level(level, test_app):
    """Test get_effective_level."""
    logger = Logging(test_app)
    logger.logger.setLevel(level)
    assert logger.get_effective_level() == level


@pytest.mark.parametrize('level', (logging.DEBUG, logging.INFO))
def test_set_level(level, test_app):
    """Test set_level."""
    logger = Logging(test_app)
    logger.set_level(level)
    assert logger.logger.getEffectiveLevel() == level
