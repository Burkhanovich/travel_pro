"""Shared pytest fixtures."""

import pytest
from django.core.cache import cache


@pytest.fixture(autouse=True)
def _clear_cache():
    """Clear the (shared, process-wide) LocMemCache between tests.

    Views like the tour list use ``cache_page``; without this, a cached
    response from an earlier test with the same URL leaks into the next one
    (and cached responses carry no ``.context`` in the test client).
    """
    cache.clear()
    yield
    cache.clear()
