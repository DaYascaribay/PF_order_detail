import os
import pytest
from run import app as flask_app

@pytest.fixture
def client():
    # ✅ Set environment variables for testing
    os.environ["ORDER_CREATION_URL"] = "http://localhost:5000/order"
    os.environ["ORDER_STATUS_URL"] = "http://localhost:5000/status"

    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client
