from builtins import Exception

from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from html2text import HTML2Text

from apps.email.models import EmailReceivers, EmailTemplate
from apps.taskqueue.celery import app

logger = get_task_logger(__name__)


@app.task(max_retries=3)
def sendmail(template_id, context, mailto, sender=settings.SENDER, subject=''):
    """
    Input parameters:
        template_id: id of template in db table 'emailtemplate'. String
        context: context of email template filling. Dict()
        mailto: email address. List of strings
        sender: senders email address. String
        subject: email subject. String
    Usage example:
        result = sendmail.delay('tmpl1', {'username': 'Mikhail'}, ['a@aaa.aa'],
                 sender='a@kkk.ru', subject='Cool letter')
    """

    html = EmailTemplate.objects.all().filter(id=template_id).first().template
    template = Template(html)
    logger.debug(template)
    html_content = template.render(Context(context))
    subject_template = Template(subject)
    subject_render = subject_template.render(Context(context))
    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = True

    text_content = h.handle(html_content)
    logger.debug(text_content)

    msg = EmailMultiAlternatives(subject_render, text_content, sender, mailto)
    msg.attach_alternative(html_content, "text/html")
    try:
        result = msg.send()
        return result
    except Exception as send_error:
        logger.error(f'Failed to send email to {mailto}. {send_error}')
        sendmail.retry(exc=send_error, countdown=1)


def send_to_receivers(message_type: str, context: dict):
    receivers = EmailReceivers.objects.filter(id=message_type)
    if not receivers.exists():
        return False
    else:
        receivers = receivers.first()
    template_id = receivers.template_id
    receivers_list = [receiver.strip() for receiver in receivers.email_list.split(',')]
    subject = receivers.subject
    sender = receivers.sender
    sendmail.delay(
        template_id,
        context,
        receivers_list,
        sender=sender,
        subject=subject
    )
    return True
