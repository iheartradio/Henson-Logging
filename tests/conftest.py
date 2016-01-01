"""Test configuration."""

import logging

import pytest


@pytest.fixture
def test_logger():
    """Return a test logger."""
    return logging.getLogger('testing')
