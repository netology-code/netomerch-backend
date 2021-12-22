from django.core.management.base import BaseCommand
from django.conf import settings
import os

from apps.products.models import ImageColorItem


class Command(BaseCommand):
    help = 'Removes orphaned imeges from disk'

    def handle(self, *args, **options):
        db_images = {imagecolor.image.name for imagecolor in ImageColorItem.objects.all()}
        image_dir = os.path.join(settings.MEDIA_ROOT, ImageColorItem.image.field.upload_to)
        image_files = set()
        for _, _, files in os.walk(image_dir):
            image_files.update(files)
        orphaned_files = image_files - db_images
        for file in orphaned_files:
            os.remove(os.path.join(image_dir, file))
