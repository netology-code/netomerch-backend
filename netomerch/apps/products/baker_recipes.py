from itertools import cycle

from model_bakery.recipe import Recipe

from apps.products.models import Category, Item, ItemProperty

category_name = ['present', 'startup', 'office', 'wear']
item_property_name = ['size', 'color', 'has_print', 'print', 'material']
item_name = ['футболка', 'блокнот', 'чашка с принтом', 'чашка айтишника',
             'чашка ПМ', 'чашка Аналитика', 'чашка Стрейнджерса']
item_published = [True, True, True, True, True, False, True]
item_props = {'color': ['black', 'white', 'yellow']}

cat_recipe = Recipe(Category, name=cycle(category_name))
prop_recipe = Recipe(ItemProperty, name=cycle(item_property_name))
item_recipe = Recipe(Item, name=cycle(item_name), is_published=cycle(item_published), properties=item_props)
