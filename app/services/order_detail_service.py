import requests
from app.config import Config

class OrderDetailService:
    def get_order_detail(self, order_id):
        # Get order data from Order Creation
        order_resp = requests.get(f"{Config.ORDER_CREATION_URL}/{order_id}")
        if order_resp.status_code == 404:
            raise ValueError("Orden no encontrada")
        elif order_resp.status_code != 200:
            raise Exception("Error en Order Creation")

        order_data = order_resp.json()

        # Get order status
        try:
            status_resp = requests.get(f"{Config.ORDER_STATUS_URL}/{order_id}")
            if status_resp.status_code == 200:
                status = status_resp.json().get("status", "PENDING")
            else:
                status = "PENDING"
        except:
            status = "PENDING"  # fallback si status service no responde

        return {
            "order_id": order_data["id"],
            "user_id": order_data["user_id"],
            "total": order_data["total"],
            "order_date": order_data.get("order_date", ""),
            "status": status,
            "items": order_data.get("items", [])
        }
