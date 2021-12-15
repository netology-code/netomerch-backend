from django.conf import settings
from django.core.management.base import BaseCommand
from openpyxl import load_workbook

from apps.products.models import Category, DictImageColor, ImageColorItem, Item, Size, Specialization


def parse_xlsx(filename):
    items = []

    wb = load_workbook(filename)
    sheet = wb[wb.sheetnames[0]]

    row = 2
    i = -1
    default_color = 0

    while row > 0:
        if sheet.cell(column=1, row=row).value is None:
            if sheet.cell(column=5, row=row).value is None:
                break
            else:
                color_tuple = [color.strip() for color in sheet.cell(column=5, row=row).value.split(',')]
                items[i]['colors'].append({
                    'color': {'name': color_tuple[0], 'code': color_tuple[1]},
                    'photos': [sheet.cell(column=j, row=row).value for j in range(7, 11)],
                    'default': len(items[i]['colors']) == default_color
                })
        else:
            i += 1
            default_color = int(sheet.cell(column=6, row=row).value) - 1
            items.append({'name': sheet.cell(column=1, row=row).value})
            items[i]['category'] = sheet.cell(column=2, row=row).value
            items[i]['specialization'] = sheet.cell(column=3, row=row).value
            items[i]['sizes'] = [size.strip() for size in sheet.cell(column=4, row=row).value.split(',')]
            items[i]['colors'] = []
            color_tuple = [color.strip() for color in sheet.cell(column=5, row=row).value.split(',')]
            items[i]['colors'].append({
                'color': {'name': color_tuple[0], 'code': color_tuple[1]},
                'photos': [sheet.cell(column=j, row=row).value for j in range(7, 11)],
                'default': len(items[i]['colors']) == default_color
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
                db_size = Size.objects.get_or_create(name=size)
                db_size = db_size[0]
                db_item.size.add(db_size)

            for color in item['colors']:
                db_color = DictImageColor.objects.get_or_create(name=color['color']['name'])
                db_color = db_color[0]
                db_color.color_code = color['color']['code']
                db_color.save()
                main_image = True
                for image in color['photos']:
                    db_image_color = ImageColorItem.objects.get_or_create(color=db_color, image=image, item=db_item)
                    db_image_color = db_image_color[0]
                    db_image_color.is_main_image = main_image
                    db_image_color.is_main_color = color['default']
                    if color['default']:
                        color['default'] = False
                    db_image_color.save()
                    main_image = False
