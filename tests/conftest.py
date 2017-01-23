"""Test configuration."""

import logging

from henson import Application
import pytest


@pytest.fixture
def test_app():
    """Return a test Application."""
    return Application('testing')


@pytest.fixture
def test_logger():
    """Return a test logger."""
    return logging.getLogger('testing')
