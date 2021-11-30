from django.core.management.base import BaseCommand

from apps.products.management.commands.load_init_category import Command as Comm_Cat


class Command(BaseCommand):
    help = 'Initial loading all around the products: categories, properties, items'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--replace', action='store_true', help='Replace template if exists', default=False)

    def handle(self, *args, **options):
        cat = Comm_Cat()
        cat.handle1(args, options)

        self.stdout.write(self.style.SUCCESS(u'Products created'))
