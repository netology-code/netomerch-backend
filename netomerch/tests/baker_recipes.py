from itertools import cycle

from model_bakery.recipe import Recipe, RecipeForeignKey, foreign_key

from apps.orders.models import Promocode
from apps.products.models import Category, DictImageColor, Item, Size, Specialization

category_name = ['Наборы', 'Футболки', 'Худи', 'Свитшоты']
item_name = ['Футболка', 'Набор', 'Худи', 'Свитшот']
item_published = [True, True, True, False]
item_hit = [True, True, False, False]
size_name = ['S', 'M', 'L']
spec_name = ['Разработка', 'Аналитика', 'Маркетинг']
color_name = ['Белый', 'Черный']
color_code = ['#FFFFFF', '#000000']

code = ['R2D2', 'BB8', 'C3PO', 'FN2187']
emails = ['mail@mail.ru', 'xex111@yandex.ru', 'xex111@yandex.ru', 'hren@mail.ru']
is_active = [True, False, True, False]

cat_recipe = Recipe(Category, name=cycle(category_name))
spec_recipe = Recipe(Specialization, name=cycle(spec_name))
size_recipe = Recipe(Size, name=cycle(size_name))
item_recipe = Recipe(Item, name=cycle(item_name),
                     is_published=cycle(item_published),
                     is_hit=cycle(item_hit),
                     category=foreign_key(cat_recipe),
                     specialization=foreign_key(spec_recipe))
color_recipe = Recipe(DictImageColor, name=cycle(color_name), color_code=cycle(color_code))

promo_recipe = Recipe(Promocode,
                      code=cycle(code),
                      email=cycle(emails),
                      is_active=cycle(is_active),
                      item=RecipeForeignKey(item_recipe, True)
                      )
