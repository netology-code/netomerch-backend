from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.email.models import EmailReceivers
from apps.email.tasks import sendmail

contact_param = openapi.Parameter('contact', openapi.IN_QUERY, type=openapi.TYPE_STRING)
name_param = openapi.Parameter('name', openapi.IN_QUERY, type=openapi.TYPE_STRING)
message_param = openapi.Parameter('message', openapi.IN_QUERY, type=openapi.TYPE_STRING)
message_type_param = openapi.Parameter('message_type', openapi.IN_QUERY, type=openapi.TYPE_STRING)

possible_responses = {'200': 'OK'}


@swagger_auto_schema('POST',
                     manual_parameters=[contact_param, name_param, message_param, message_type_param],
                     responses=possible_responses)
@api_view(['POST'])
def callback(request):
    receivers = EmailReceivers.objects.get(id=request.query_params.get('message_type'))
    context = {key: value for key, value in request.query_params.items()}
    template_id = receivers.template_id
    receivers = [receiver.strip() for receiver in receivers.email_list.split(',')]
    sendmail.delay(
        template_id,
        context,
        receivers,
        sender='a@kkk.ru',
        subject='Callback message from site'
    )
    return Response('OK', status=200)
