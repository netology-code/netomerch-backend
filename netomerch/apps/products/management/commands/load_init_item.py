import json

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.products.models import Category, Item


class Command(BaseCommand):
    help = 'Initial loading products'' items'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--replace', action='store_true', help='Replace template if exists', default=False)

    def handle1(self, args, options):
        with open(settings.BASE_DIR / "apps/products/management/data/items.json", encoding='utf-8') as f:
            data = json.load(f)
        for x in data["items"]:
            if options["replace"]:
                Item.objects.filter(name=x['name']).delete()

            if Item.objects.filter(name=x['name']).count() == 0:

                item = Item(name=x['name'], price=x['price'], is_published=x['is_published'],
                            is_hit=x['is_hit'], properties=x['properties'])
                item.save()
                for cat in x['category']:
                    cat_obj = Category.objects.filter(name=cat).all().values().get()['id']
                    item.category.add(cat_obj)

                self.stdout.write(self.style.SUCCESS(u'Item %s has been created' % (x["name"])))

    def handle(self, *args, **options):
        self.handle1(args, options)
