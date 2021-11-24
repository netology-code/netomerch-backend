from builtins import Exception

from celery.utils.log import get_task_logger
from django.core.mail import EmailMultiAlternatives
from django.template import Context, Template
from html2text import HTML2Text

from apps.email.models import EmailTemplate
from apps.taskqueue.celery import app

logger = get_task_logger(__name__)


@app.task(max_retries=3)
def sendmail(template_id, context, mailto, sender=None, subject=''):
    """
    Input parameters:
        template_id: id of template in db table 'emailtemplate'
        context: context of email template filling. Dict()
        mailto: email address. Text
        sender: senders email address. Text
        subject: email subject. Text
    Usage example:
        result = sendmail.delay('tmpl1', {'username': 'Mikhail'}, 'a@aaa.aa',
                 sender='a@kkk.ru', subject='Cool letter')
    """

    html = EmailTemplate.objects.all().filter(id=template_id).first().template
    template = Template(html)
    logger.debug(template)
    html_content = template.render(Context(context))
    h = HTML2Text()
    h.ignore_links = False
    h.ignore_images = True

    text_content = h.handle(html_content)
    logger.debug(text_content)

    msg = EmailMultiAlternatives(subject, text_content, sender, mailto)
    msg.attach_alternative(html_content, "text/html")
    try:
        result = msg.send()
        return result
    except Exception as send_error:
        logger.error(f'Failed to send email to {mailto}. {send_error}')
        sendmail.retry(exc=send_error, countdown=1)
