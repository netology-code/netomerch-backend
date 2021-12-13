from rest_framework import mixins
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
        #
        # email = order.data['email']
        # total_sum = order.data['total_sum']
        # final_sum = order.data['final_sum']
        # template_id = 'new_order'
        #
        # items = []
        #
        # for it in order.data['item']:
        #     it = dict(it)
        #     item = Item.objects.filter(id=it['items']).values('id', 'name', 'price')[0]
        #
        #     item_sum = it['count'] * item['price']
        #     items.append(
        #         {'item_name': item['name'],
        #          'item_price': item['price'],
        #          'item_count': f"x{it['count']}",
        #          'item_sum': item_sum}
        #     )
        #
        # context = {
        #     'name': order.data['name'],
        #     'order_id': order.data['id'],
        #     'items': items,
        #     'final_sum': final_sum
        # }
        #
        # if total_sum != final_sum:
        #     discount = float(total_sum) - float(final_sum)
        #     context = {**{'discount': discount, 'total_sum': total_sum}, **context}
        #     template_id = 'new_order2'
        #
        # sendmail.delay(
        #     template_id=template_id,
        #     context=context,
        #     mailto=[email],
        #     subject=f'Заказ № {order.data["id"]}'
        # )
        return order
