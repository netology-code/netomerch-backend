import json

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.products.models import ItemProperty


class Command(BaseCommand):
    help = 'Initial loading items'' properties'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--replace', action='store_true', help='Replace template if exists', default=False)

    def handle1(self, args, options):
        with open(settings.BASE_DIR / "apps/products/management/data/itemproperties.json", encoding='utf-8') as f:
            data = json.load(f)
        for x in data["itemproperties"]:
            if options["replace"]:
                ItemProperty.objects.filter(name=x['name']).delete()

            if ItemProperty.objects.filter(name=x['name']).count() == 0:
                ItemProperty(name=x['name'], type=x['type'], description=x['description']).save()
                self.stdout.write(self.style.SUCCESS(u'ItemProperty %s has been created' % (x["name"])))

    def handle(self, *args, **options):
        self.handle1(args, options)
