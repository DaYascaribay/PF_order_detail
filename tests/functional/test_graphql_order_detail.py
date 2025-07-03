from app import app

def test_graphql_order_detail(client, requests_mock):
    order_data = {
        "id": 1,
        "user_id": 10,
        "total": 99.99,
        "order_date": "2025-07-03T10:00:00Z",
        "items": [{"product_id": 1, "quantity": 2, "price": 49.99}]
    }
    status_data = {"status": "PAID"}

    requests_mock.get("http://localhost:5000/order/1", json=order_data)
    requests_mock.get("http://localhost:5000/status/1", json=status_data)

    query = """
    {
        orderDetail(orderId: 1) {
            orderId
            userId
            total
            orderDate
            status
            items {
                productId
                quantity
                price
            }
        }
    }
    """

    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json["data"]["orderDetail"]
    assert data["status"] == "PAID"
    assert data["orderId"] == 1
