import graphene

class OrderItemType(graphene.ObjectType):
    product_id = graphene.Int()
    quantity = graphene.Int()
    price = graphene.Float()

class OrderDetailType(graphene.ObjectType):
    order_id = graphene.Int()
    user_id = graphene.Int()
    total = graphene.Float()
    order_date = graphene.String()
    status = graphene.String()
    items = graphene.List(OrderItemType)
