import json

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.email.models import EmailReceivers, EmailTemplate


class Command(BaseCommand):
    help = 'Initial loading templates for emails'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--replace', action='store_true', help='Replace template if exists', default=False)

    def handle(self, *args, **options):
        with open(settings.BASE_DIR / "apps/email/management/data/templates.json", encoding='utf-8') as f:
            data = json.load(f)

        for x in data["templates"]:
            if options["replace"]:
                EmailTemplate.objects.filter(id=x["id"]).delete()
                EmailReceivers.objects.filter(template_id=x["id"]).delete()

            if EmailTemplate.objects.filter(id=x["id"]).count() == 0:
                EmailTemplate(id=x["id"], description=x["description"], template=x["template"]).save()
                self.stdout.write(self.style.SUCCESS(u'Template %s has been created' % (x["id"])))

            if EmailReceivers.objects.filter(template_id=x["id"]).count() == 0:
                EmailReceivers(id=x["id"],
                               description=x["description"],
                               template=EmailTemplate.objects.get(id=x["id"]),
                               subject=x["subject"],
                               sender=x["sender"],
                               email_list=x["email_list"]).save()
                self.stdout.write(self.style.SUCCESS(u'Receivers for template %s has been created' % (x["id"])))
