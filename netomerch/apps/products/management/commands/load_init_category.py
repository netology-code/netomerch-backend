import json

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.products.models import Category


class Command(BaseCommand):
    help = 'Initial loading products'' categories'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--replace', action='store_true', help='Replace template if exists', default=False)

    def handle1(self, args, options):
        with open(settings.BASE_DIR / "apps/products/management/data/categories.json", encoding='utf-8') as f:
            data = json.load(f)
        for x in data["categories"]:
            if options["replace"]:
                Category.objects.filter(name=x['name']).delete()

            if Category.objects.filter(name=x['name']).count() == 0:
                Category(name=x['name'], short_description=x['short_description'],
                         description=x['description'], image=x['image']).save()
                self.stdout.write(self.style.SUCCESS(u'Category %s has been created' % (x["name"])))

    def handle(self, *args, **options):
        self.handle1(args, options)
