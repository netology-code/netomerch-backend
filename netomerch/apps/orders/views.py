from rest_framework.decorators import api_view
from rest_framework.response import Response


from apps.email.tasks import sendmail


@api_view(['POST'])
def send_email(request):
    result = sendmail.delay(
        'tmpl1',
        {
            'username': 'Mikhail',
            'als': [
                'one',
                'two',
                'three',
            ]

        },
        'a@aaa.aa',
        sender='a@kkk.ru',
        subject='hhhhaa hhha hha'
    )
    return Response({
        'id': result.id,
        'result': result.status,
    })
