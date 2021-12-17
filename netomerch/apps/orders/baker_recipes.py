from itertools import cycle

from model_bakery.recipe import Recipe, foreign_key, RecipeForeignKey
from apps.products.baker_recipes import item_recipe

from apps.orders.models import Promocode

code = ['R2D2', 'BB8', 'C3PO', 'FN2187']
emails = ['mail@mail.ru', 'xex111@yandex.ru', 'netology@gmail.com', 'hren@mail.ru']
is_active = [True, False, True, False]

promo_recipe = Recipe(Promocode,
                      code=cycle(code),
                      email=cycle(emails),
                      is_active=cycle(is_active),
                      item=RecipeForeignKey(item_recipe, True)
                      )
