import graphene
from app.types.order_type import OrderDetailType, OrderItemType
from app.services.order_detail_service import OrderDetailService

class Query(graphene.ObjectType):
    order_detail = graphene.Field(OrderDetailType, order_id=graphene.Int(required=True))

    def resolve_order_detail(self, info, order_id):
        service = OrderDetailService()
        try:
            return service.get_order_detail(order_id)
        except ValueError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception("Error interno al obtener detalle de orden")

schema = graphene.Schema(query=Query)
