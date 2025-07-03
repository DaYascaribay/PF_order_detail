# tests/conftest.py
import os
import pytest

# Set the required env vars before importing the app
os.environ["ORDER_CREATION_URL"] = "http://localhost:5000/order"
os.environ["ORDER_STATUS_URL"] = "http://localhost:5000/status"

from run import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

