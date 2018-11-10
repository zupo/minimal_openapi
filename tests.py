from pyramid.router import Router
from run import app
from webtest import TestApp

import os
import pytest


@pytest.fixture(scope="session")
def testapp() -> TestApp:
    """Provide a webtest app for functional testing."""
    return TestApp(app())


def test_foo(testapp):
    """Error message for missing field."""
    resp = testapp.get("/api/v1/todo/", status=[200])
    assert resp.json_body == [{"title": "Buy milk"}]
