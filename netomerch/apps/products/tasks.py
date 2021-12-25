import os

import gdown
from celery.utils.log import get_task_logger
from django.core.files import File

from apps.products.models import ImageColorItem
from apps.taskqueue.celery import app

logger = get_task_logger(__name__)


@app.task(max_retries=3, rate_limit="10/m")
def download_image(id, g_url):
    try:
        db_image_color = ImageColorItem.objects.get(id=id)
        file = gdown.download(g_url, fuzzy=True)
        with open(file, 'rb') as f:
            db_image_color.image = File(f)
            db_image_color.save()
        os.remove(f.name)
    except Exception as exc:
        logger.error('exc')
        download_image.retry(exc=exc, countdown=1)


@app.task(max_retries=3)
def remove_image_file(filename):
    try:
        os.remove(filename)
    except Exception as exc:
        logger.error(f'Error removing old file: {exc}')
        remove_image_file.retry(exc=exc, countdown=1)
