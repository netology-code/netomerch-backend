from django.contrib import admin

from apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['orders_item']

    model = Review
    list_display = ("id", "author", "email", 'text', 'is_published')

    def review_id(self, obj):
        return f'Отзыв № {obj.id}'
