from jflask import parse_json, parse_query
from flask import Flask
import pytest
import inspect
import json

app = Flask(__name__)


def func_path() -> str:
    """
    Generate a route path based on the function's name
    :return str: route path
    """
    return f"/{inspect.stack()[1][3]}"


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_func_path_helper():
    assert func_path() == "/test_func_path_helper"


def test_sanity_check(client):
    app.add_url_rule(func_path(), view_func=lambda: ("pong", 200))
    resp = client.get(func_path())
    assert b'pong' in resp.data and resp.status_code == 200


def test_parse_json(client):
    @parse_json("body")
    def test_parse_json_view(body):
        return f"Hello, {body.get('first_name', '')}!", 200

    app.add_url_rule(func_path(), methods=["POST"], view_func=test_parse_json_view)
    resp = client.post(func_path(), data=json.dumps(dict(first_name="jane")))
    assert resp.data == b'Hello, jane!' and resp.status_code == 200

    resp = client.post(func_path(), data=json.dumps(dict(last_name="doe")))
    assert resp.data == b'Hello, !' and resp.status_code == 200


def test_parse_json_required_fields(client):
    @parse_json("body", required_fields=["first_name", "last_name"])
    def test_parse_json_required_fields_view(body):
        return f"Hello, {body.get('first_name')} {body.get('last_name')}!", 200

    app.add_url_rule(func_path(), methods=["POST"], view_func=test_parse_json_required_fields_view)
    resp = client.post(func_path(), data=json.dumps(dict(first_name="jane", last_name="doe")))
    assert resp.data == b'Hello, jane doe!' and resp.status_code == 200

    resp = client.post(func_path(), data=json.dumps(dict(first_name="john")))
    assert b'missing required' in resp.data and resp.status_code == 400


def test_parse_query(client):
    @parse_query("params")
    def test_parse_query_view(params):
        return f"Hello, {params.get('first_name', '')}!", 200

    app.add_url_rule(func_path(), view_func=test_parse_query_view)
    resp = client.get(f"{func_path()}?first_name=jane")
    assert resp.data == b'Hello, jane!' and resp.status_code == 200

    resp = client.get(f"{func_path()}?last_name=doe")
    assert resp.data == b'Hello, !' and resp.status_code == 200


def test_parse_query_required_fields(client):
    @parse_query("params", required_fields=["first_name", "last_name"])
    def test_parse_query_required_fields_view(params):
        return f"Hello, {params.get('first_name')} {params.get('last_name')}!"

    app.add_url_rule(func_path(), view_func=test_parse_query_required_fields_view)
    resp = client.get(f"{func_path()}?first_name=jane&last_name=doe")
    assert resp.data == b'Hello, jane doe!' and resp.status_code == 200

    resp = client.get(f"{func_path()}?first_name=jane")
    assert b'missing required' in resp.data and resp.status_code == 400
