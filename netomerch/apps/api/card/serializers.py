from django.conf import settings
from rest_framework import serializers

from apps.products.models import ImageColorItem, Item, Size
from apps.reviews.models import Review


class CardSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source="id")
    sizes = serializers.SerializerMethodField()
    colors = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def _get_path(self, file):
        request = self.context.get('request')
        return str(request.build_absolute_uri("/")) + str(settings.MEDIA_URL)[1:] + file

    class Meta:
        model = Item
        fields = ("reviews", "item_id", "name", "description", "price", "colors", "sizes", )

    def get_reviews(self, item):
        review_data = Review.objects.filter(item=item.id, is_published=True).values().all()
        reviews = list()
        for review in review_data:
            reviews.append({"id": review["id"],
                            "text": review["text"],
                            "author": review["author"],
                            "author_image": "",
                            "date": "2021-12-20 08:50:55"})
        return reviews

    def get_sizes(self, item):
        sizes = list()
        for size in list(Size.objects.filter(item=item).values("name").all()):
            sizes.append(size["name"])
        return sizes

    def get_colors(self, item):
        result = list()

        # Main_color
        images = list()
        data = ImageColorItem.objects.filter(
            item_id=item.id, is_main_color=True). \
            values_list("color_id", "color_id__name", "color_id__name_eng",
                        "color_id__color_code", "is_main_color").all()
        main_color_id = data[0][0]
        images_info = list(ImageColorItem.objects.filter(item_id=item.id, color_id=main_color_id).
                           values_list("is_main_image", "image").all())
        for image in images_info:
            images.append({"is_main": image[0], "images": self._get_path(image[1])})
        result.append({"name": data[0][1],
                       "is_main": data[0][4],
                       "name_eng": data[0][2],
                       "color_code": data[0][3],
                       "images": images})

        # other colors
        data = list(ImageColorItem.objects.filter(
            item_id=item.id, is_main_color=False).exclude(color_id=main_color_id).
            distinct("color_id", "color_id__name", "color_id__name_eng", "color_id__color_code", "is_main_color").
            values_list("color_id", "color_id__name", "color_id__name_eng",
                        "color_id__color_code", "is_main_color").all())

        for color_info in data:
            images_info = list(ImageColorItem.objects.filter(item_id=item.id, color_id=color_info[0]).
                               values_list("is_main_image", "image").all())
            images = list()
            for image in images_info:
                images.append({"is_main": image[0], "images": self._get_path(image[1])})

            result.append({"name": color_info[1],
                           "is_main": color_info[4],
                           "name_eng": color_info[2],
                           "color_code": color_info[3],
                           "images": images})

        return result
