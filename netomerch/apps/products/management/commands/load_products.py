from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from apps.products.models import Category, DictImageColor, ImageColorItem, Item, Size, Specialization
from apps.products.tasks import download_image


def parse_xlsx(filename):
    items = dict()

    wb = load_workbook(filename)
    sheet = wb[wb.sheetnames[0]]

    row = 2

    while row > 0:
        print("row", row)
        if not sheet.cell(column=1, row=row).value:
            break
        default_color = sheet.cell(column=8, row=row).value is not None
        name = sheet.cell(column=1, row=row).value
        specialization = sheet.cell(column=3, row=row).value
        if (name, specialization) not in items:
            items[(name, specialization)] = {
                "name": name,
                "specialization": specialization,
                "colors": [],
            }
        items[(name, specialization)]['category'] = sheet.cell(column=2, row=row).value
        items[(name, specialization)]['sizes'] = [
            size.strip() for size in sheet.cell(column=4, row=row).value.split(',')
        ]
        color_tuple = [color.strip() for color in sheet.cell(column=5, row=row).value.split(',')]
        items[(name, specialization)]['colors'].append({
            'color': {'name': color_tuple[0], 'code': color_tuple[1]},
            'images': [sheet.cell(column=j, row=row).value for j in range(9, 13)],
            'default': default_color
        })
        items[(name, specialization)]['description'] = sheet.cell(column=6, row=row).value
        items[(name, specialization)]['short_description'] = sheet.cell(column=7, row=row).value
        items[(name, specialization)]['is_hit'] = sheet.cell(column=14, row=row).value is not None
        price = sheet.cell(column=15, row=row).value
        items[(name, specialization)]['price'] = float(price) if price is not None else 0.0

        row += 1
    return items


class Command(BaseCommand):
    help = 'Loads items from xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        items = parse_xlsx(options['filename'][0])
        for _, item in items.items():
            category = Category.objects.get_or_create(name=item['category'])[0]

            specialization = Specialization.objects.get_or_create(name=item['specialization'])[0]

            db_item = Item.objects.get_or_create(name=item['name'],
                                                 category=category,
                                                 specialization=specialization)
            db_item = db_item[0]

            db_item.description = item['description']
            db_item.short_description = item['short_description']

            db_item.price = item['price']
            db_item.is_hit = item['is_hit']
            db_item.save()

            image_color_items_to_delete = ImageColorItem.objects.filter(item=db_item)
            image_color_items_to_delete.delete()
            db_item.size.all().delete()

            for size in item['sizes']:
                db_size = Size.objects.get_or_create(name=size.capitalize())
                db_size = db_size[0]
                db_item.size.add(db_size)

            for color in item['colors']:
                db_color = DictImageColor.objects.get_or_create(name=color['color']['name'].capitalize())
                db_color = db_color[0]
                db_color.color_code = color['color']['code']
                db_color.save()
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
                    db_image_color.save()
                    download_image.delay(db_image_color.id, image)
                    main_image = False
