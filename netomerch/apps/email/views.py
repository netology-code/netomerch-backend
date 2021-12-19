from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.email.tasks import send_to_receivers

schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'contact': openapi.Schema(type=openapi.TYPE_STRING, description='Sender contact data'),
        'name': openapi.Schema(type=openapi.TYPE_STRING, description='Sender name'),
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message from sender'),
    }
)
possible_responses = {'200': 'OK', '4xx': 'Not OK'}


@swagger_auto_schema('POST',
                     request_body=schema,
                     responses=possible_responses,
                     operation_description='A testing schema for callback route. '
                                           'Watch the results at http://dev.nemerch.tk/mailhog/')
@api_view(['POST'])
def callback(request):
    message_type = "callback"
    context = request.data
    if send_to_receivers(message_type, context):
        return Response('OK', status=200)
    else:
        return Response('Template callback not found!', status=404)
