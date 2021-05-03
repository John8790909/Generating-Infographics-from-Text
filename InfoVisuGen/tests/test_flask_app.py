"""
    script: test_flask_app.py 
    description: automatised way to check for any problems encountered in Flask app's API
"""
import pytest
import sys

@pytest.fixture
def client():
    try:
        import app
        with app.app.test_client() as client:
            yield client
    except LookupError:
        assert False, 'failed to import app'


def test_main_url(client):
    resp = client.get('/')
    assert resp == 200
