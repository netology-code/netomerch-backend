import imghdr
import os
from hashlib import md5
from random import randbytes

import gdown
from celery.utils.log import get_task_logger

from apps.products.models import ImageColorItem
from apps.taskqueue.celery import app

logger = get_task_logger(__name__)


@app.task(max_retries=3, rate_limit="10/m")
def download_image(id, g_url):
    db_image_color = ImageColorItem.objects.get(id=id)
    file_path = db_image_color.image.field.storage.location
    upload_to = db_image_color.image.field.upload_to
    r = randbytes(255)
    filename = md5(r).hexdigest()
    full_path = os.path.join(file_path, upload_to, filename)

    gdown.download(g_url, fuzzy=True, output=full_path)
    ext = imghdr.what(full_path)
    os.rename(full_path, f'{full_path}.{ext}')
    db_image_color.image = f'/{upload_to}/{filename}.{ext}'
    db_image_color.save()
