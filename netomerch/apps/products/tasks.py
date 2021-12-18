from celery.utils.log import get_task_logger
import gdown
import imghdr
import os

from apps.products.models import ImageColorItem
from apps.taskqueue.celery import app

logger = get_task_logger(__name__)


@app.task(max_retries=3, rate_limit="10/m")
def download_image(id, g_url):
    db_image_color = ImageColorItem.objects.get(id=id)
    filename = f'media/item/{db_image_color.id}'
    gdown.download(g_url, fuzzy=True, output=filename)
    ext = imghdr.what(filename)
    os.rename(filename, f'{filename}.{ext}')
    db_image_color.image = f'/item/{db_image_color.id}.{ext}'
    db_image_color.save()
    pass
