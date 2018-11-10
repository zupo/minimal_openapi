from run import app
from webtest import TestApp

import os
import pytest


@pytest.fixture(scope="session")
def testapp() -> TestApp:
    """Provide a webtest app for functional testing."""
    return TestApp(app())


def test_todo_app(testapp):
    """Test posting TODO items and then getting them."""
    resp = testapp.get("/api/v1/todo/", status=[200])
    assert resp.json_body == [{"title": "Buy milk"}]

    resp = testapp.post_json("/api/v1/todo/", {"title": "Walk the dog"}, status=[200])
    assert resp.json_body == [{"message": "Item added"}]

    resp = testapp.get("/api/v1/todo/", status=[200])
    assert resp.json_body == [{"title": "Buy milk"}, {"title": "Walk the dog"}]


def test_validation(testapp):
    """Test that bad requests are handled."""

    # empty body
    resp = testapp.post_json("/api/v1/todo/", {}, status=[400])
    assert resp.json_body == ["Mimetype invalid: Missing schema property: title"]

    # bad field
    resp = testapp.post_json("/api/v1/todo/", {"foo": "bar"}, status=[400])
    assert resp.json_body == [
        "Mimetype invalid: Extra unexpected properties found in schema: {'foo'}"
    ]

    # title too long
    resp = testapp.post_json("/api/v1/todo/", {"title": "1234567890" * 5}, status=[400])
    assert resp.json_body == [
        "Mimetype invalid: Invalid schema property title: Value is longer (50)"
        " than the maximum length of 40"
    ]
