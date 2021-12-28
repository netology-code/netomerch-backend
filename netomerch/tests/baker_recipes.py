from itertools import cycle

from model_bakery.recipe import Recipe, RecipeForeignKey, foreign_key

from apps.orders.models import Order, Promocode
from apps.products.models import Category, DictImageColor, Item, Size, Specialization
from apps.reviews.models import Review

"""Products data"""
category_name = ['Наборы', 'Футболки', 'Худи', 'Свитшоты']
item_name = ['Футболка', 'Набор', 'Худи', 'Свитшот']
item_published = [True, True, True, False]
item_hit = [True, True, False, False]
size_name = ['S', 'M', 'L']
spec_name = ['Разработка', 'Аналитика', 'Маркетинг']
color_name = ['Белый', 'Черный']
color_code = ['#FFFFFF', '#000000']

"""Review data"""
review_text = ['Текст1', 'Текст2', 'Текст3', 'Текст4']

"""Promo data"""
code = ['R2D2', 'BB8', 'C3PO', 'FN2187']
emails = ['mail@mail.ru', 'xex111@yandex.ru', 'xex111@yandex.ru', 'hren@mail.ru']
is_active = [True, False, True, False]

"""Order data"""
order_name = ['Коля', 'Паша', 'Миша', 'Макс']
phone_field = ['+79999999999', '+79888888888', '+79888888887', '+79888888886']

"""Recipe for products"""
cat_recipe = Recipe(Category, name=cycle(category_name))
spec_recipe = Recipe(Specialization, name=cycle(spec_name))
size_recipe = Recipe(Size, name=cycle(size_name))
item_recipe = Recipe(Item, name=cycle(item_name),
                     is_published=cycle(item_published),
                     is_hit=cycle(item_hit),
                     category=foreign_key(cat_recipe),
                     specialization=foreign_key(spec_recipe))
color_recipe = Recipe(DictImageColor, name=cycle(color_name), color_code=cycle(color_code))

"""Recipe for promo"""
promo_recipe = Recipe(Promocode,
                      code=cycle(code),
                      email=cycle(emails),
                      is_active=cycle(is_active),
                      item=RecipeForeignKey(item_recipe, True)
                      )

"""Recipe for order"""
order_recipe = Recipe(Order,
                      name=cycle(order_name),
                      phone=cycle(phone_field))

"""Recipe for review"""
review_recipe = Recipe(Review,
                       text=review_text,
                       order=RecipeForeignKey(order_recipe, True),
                       item=RecipeForeignKey(item_recipe, True))
