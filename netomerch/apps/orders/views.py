from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.models import Item
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):

        orders = Order.objects.order_by('pk').all().prefetch_related('items')
        return orders

    def create(self, request, *args, **kwargs):
        data = request.data
        name = data['name']
        email = data['email']
        phone = data['phone']
        if 'promo' in data.keys():
            promo = data['promo']
            new_order = Order.objects.create(name=name, email=email, phone=phone, promo=promo)
        else:
            new_order = Order.objects.create(name=name, email=email, phone=phone)

        new_order.save()

        for item in data['items']:
            item_obj = Item.objects.get(orders__pk=item['id'])
            new_order.items.add(item_obj)

        serializer = OrderSerializer(new_order)
        return Response(serializer.data)

