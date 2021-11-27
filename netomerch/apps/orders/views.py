from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.email.tasks import sendmail
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.products.models import Item


class OrderViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        order = super().create(request, *args, **kwargs)

        email = order.data['email']
        items = []
        total_sum = order.data['total_sum']
        final_sum = order.data['final_sum']
        if total_sum == final_sum:
            discount = total_sum - final_sum

        for it in order.data['item']:
            it = dict(it)
            item = Item.objects.filter(id=it['items']).values('id', 'name', 'price')[0]

            item_sum = it['count'] * item['price']
            items.append(
                {'item_name': item['name'],
                 'item_price': item['price'],
                 'item_count': f"x{it['count']}",
                 'item_sum': item_sum}
            )

        context = {
            'name': order.data['name'],
            'order_id': order.data['id'],
            'items': items,
            'total_sum': total_sum,
            'final_sum': final_sum
        }

        sendmail.delay(
            template_id='new_order',
            context=context,
            mailto=[email],
            subject=f'Заказ № {order.data["id"]}'
        )
        return Response(order.data)
