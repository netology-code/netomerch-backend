from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.api.card.serializers import CardSerializer
from apps.api.orders.serializers import OrderSerializer
from apps.email.tasks import sendmail
from apps.orders.models import Order, Promocode
from apps.products.models import Item


class OrderViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []

    @swagger_auto_schema(operation_description='PhoneFormat: +79999999999')
    def create(self, request, *args, **kwargs):
        order = super().create(request, *args, **kwargs)
        self.send_order_mail(order)
        return order

    def send_order_mail(self, order):
        email = order.data['email']
        total_sum = order.data['total_sum']
        final_sum = order.data['final_sum']
        template_id = 'new_order'

        items = []

        for item in order.data['items']:
            item = dict(item)
            item_info = Item.objects.filter(id=item['item_id']).values('id', 'name')[0]

            item_sum = item['count'] * item['price']
            items.append(
                {'item_name': item_info['name'],
                 'item_price': item['price'],
                 'item_count': f"x{item['count']}",
                 'item_sum': item_sum}
            )

        context = {
            'name': order.data['name'],
            'order_id': order.data['id'],
            'items': items,
            'final_sum': final_sum
        }

        if total_sum != final_sum:
            discount = float(total_sum) - float(final_sum)
            context = {**{'discount': discount, 'total_sum': total_sum}, **context}
            template_id = 'new_order2'

        sendmail.delay(
            template_id=template_id,
            context=context,
            mailto=[email],
            subject=f'Заказ № {order.data["id"]}'
        )


class PromocodeView(APIView):
    authentication_classes = []

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        },
        required=['code', 'email']
    ))
    def post(self, request, *args, **kwargs):
        promo = Promocode.objects.filter(code=request.data['code']).first()
        if promo is None or promo.is_active is False:
            raise ValidationError("Incorrect code or email", code=status.HTTP_400_BAD_REQUEST)
        elif promo.email != request.data['email']:
            raise ValidationError("Incorrect code or email", code=status.HTTP_400_BAD_REQUEST)
        item = Item.objects.filter(is_published=True).filter(pk=promo.item.id).first()
        serializer = CardSerializer(item, context={"request": request})

        item = serializer.data
        item.pop('reviews')

        response = {**{'code': request.data['code']}, **{'item': item}}

        return Response(response, status=status.HTTP_200_OK)
