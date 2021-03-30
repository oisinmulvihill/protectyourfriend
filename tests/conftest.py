import logging

import pytest

from webapp.app_logging import log_setup


@pytest.fixture(scope="module")
def log():
    """Set up logging as a pytest fixture."""
    log_setup()
    return logging.getLogger('protectyourfriend')
