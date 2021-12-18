from celery.utils.log import get_task_logger
from google_drive_downloader import GoogleDriveDownloader as gdd

from apps.products.models import ImageColorItem
from apps.taskqueue.celery import app

logger = get_task_logger(__name__)


@app.task(max_retries=3, rate_limit="3/m")
def download_image(id, g_url):
    db_image_color = ImageColorItem.objects.get(id=id)
    file_id = g_url.split('/')[-2]
    gdd.download_file_from_google_drive(file_id, dest_path=f'media/item/{db_image_color.id}image.jpg')
    db_image_color.image = f'/item/{db_image_color.id}image.jpg'
    db_image_color.save()
    pass
