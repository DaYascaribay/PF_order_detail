from unittest.mock import patch
from app.services.order_detail_service import OrderDetailService

@patch("app.services.order_detail_service.requests.get")
def test_get_order_detail_success(mock_get):
    mock_order_data = {
        "id": 1,
        "user_id": 10,
        "total": 99.99,
        "order_date": "2025-07-03T10:00:00Z",
        "items": [
            {"product_id": 1, "quantity": 2, "price": 49.99}
        ]
    }

    mock_status_data = {"status": "PAID"}

    mock_get.side_effect = [
        MockResponse(mock_order_data, 200),
        MockResponse(mock_status_data, 200)
    ]

    service = OrderDetailService()
    result = service.get_order_detail(1)

    assert result["status"] == "PAID"
    assert result["order_id"] == 1
    assert result["user_id"] == 10
    assert result["total"] == 99.99

class MockResponse:
    def __init__(self, json_data, status_code):
        self._json = json_data
        self.status_code = status_code

    def json(self):
        return self._json
