from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from apps.products.models import Category, DictImageColor, ImageColorItem, Item, Size, Specialization
from apps.products.tasks import download_image


def parse_xlsx(filename):
    items = []

    wb = load_workbook(filename)
    sheet = wb[wb.sheetnames[0]]

    row = 2

    while row > 0:
        print("row", row)
        if not sheet.cell(column=1, row=row).value:
            break
        default_color = sheet.cell(column=8, row=row).value is not None
        items.append({'name': sheet.cell(column=1, row=row).value})
        items[-1]['category'] = sheet.cell(column=2, row=row).value
        items[-1]['specialization'] = sheet.cell(column=3, row=row).value
        items[-1]['sizes'] = [size.strip() for size in sheet.cell(column=4, row=row).value.split(',')]
        items[-1]['colors'] = []
        color_tuple = [color.strip() for color in sheet.cell(column=5, row=row).value.split(',')]
        items[-1]['colors'].append({
            'color': {'name': color_tuple[0], 'code': color_tuple[1]},
            'images': [sheet.cell(column=j, row=row).value for j in range(9, 13)],
            'default': default_color
        })
        row += 1
    return items


class Command(BaseCommand):
    help = 'Loads items from xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        items = parse_xlsx(options['filename'][0])
        for item in items:
            category = Category.objects.get_or_create(name=item['category'])[0]

            specialization = Specialization.objects.get_or_create(name=item['specialization'])[0]

            db_item = Item.objects.get_or_create(name=item['name'],
                                                 category=category,
                                                 specialization=specialization)
            db_item = db_item[0]

            for size in item['sizes']:
                db_size = Size.objects.get_or_create(name=size.capitalize())
                db_size = db_size[0]
                db_item.size.add(db_size)
                db_item.imagecolor.all().delete()

            for color in item['colors']:
                db_color = DictImageColor.objects.get_or_create(name=color['color']['name'].capitalize())
                db_color = db_color[0]
                db_color.color_code = color['color']['code']
                db_color.save(force_update=True)
                main_image = True
                i = 0
                for image in color['images']:
                    tmp_image = f'no_image_{i}'
                    i += 1
                    db_image_color = ImageColorItem.objects.get_or_create(color=db_color, item=db_item, image=tmp_image)
                    db_image_color = db_image_color[0]
                    db_image_color.is_main_image = main_image
                    db_image_color.is_main_color = color['default']
                    db_image_color.image = tmp_image
                    if color['default']:
                        color['default'] = False
                    db_image_color.save(force_update=True)
                    download_image.delay(db_image_color.id, image)
                    main_image = False
