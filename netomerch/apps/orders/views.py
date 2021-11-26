from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.email.tasks import sendmail
from apps.products.models import Item, Image


class OrderViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        order = super().create(request, *args, **kwargs)

        email = order.data['email']
        items = []
        main_sum = 0
        for it in order.data['item']:
            it = dict(it)
            item = Item.objects.filter(id=it['items']).values('id', 'name', 'price')[0]
            image = Image.objects.filter(items=it['items']).values_list('image', flat=True)[0]

            items.append(
                {'item_name': item['name'],
                 'item_image': image,
                 'item_sum': f"{it['count']} x {item['price']}"}
            )
            main_sum += it['count'] * item['price']

        context = {
            'name': order.data['name'],
            'order_id': order.data['id'],
            'items': items,
            'main_sum': main_sum
        }

        sendmail.delay(
            template_id='new_order',
            context=context,
            mailto=[email],
            subject=f'Заказ № {order.data["id"]}'
        )
        return Response(order.data)
