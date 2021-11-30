from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.email.tasks import sendmail
from apps.products.models import Category, Item, Review
from apps.products.permissions import IsAdmin
from apps.products.serializers import (
    CategorySerializer,
    ItemSerializer,
    ReviewSerializer,
    SendReviewSerializer,
)


class BaseViewSet:
    """только админ может удалять, обновлять, создавать, а просматривать могут все"""

    def get_permissions(self):
        """Получение прав для действий"""

        # FIXME: здесь показывает предупреждение, но всё ок. Наследование ModelViewSet нельзя сюда в класс добавить
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAdmin()]
        return []


@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='retrieve')
class CategoryViewSet(BaseViewSet, ModelViewSet):
    """
    Энд-поинт категорий товаров - /api/v1/categories/
    Доступные методы
    - GET - доступно всем
    - POST, PATCH, DELETE - только Админу, остальным 403 запрещено
    """
    queryset = Category.objects.order_by('pk').all()

    serializer_class = CategorySerializer

    search_fields = ['name', 'id']  # поля, по которым доступен поиск ?search=что-то


@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='retrieve')
class ItemViewSet(BaseViewSet, ModelViewSet):
    """
    Энд-поинт товаров (продуктов) - /api/v1/items/
    Доступные методы
    - GET - доступно всем, админы видят все товары, остальные только те, которые is_published
    - POST, PATCH, DELETE - только Админу, остальным 403 запрещено
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    search_fields = ['name']  # поля, по которым доступен поиск ?search=что-то
    filterset_fields = ('category__name', )

    def get_queryset(self):
        """переопределяем кверисет: админ (видит все товары) или не-админ (видят только опубликованные)"""
        if self.request.user.is_superuser:
            queryset = Item.objects.order_by('pk').all().prefetch_related('category')
        else:
            queryset = Item.objects.filter(is_published=True).order_by('pk').all().prefetch_related('category')
        return queryset


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    end-point for reviews - /api/v1/reviews/
    Can use these methods:
    - GET - for everyone (but admin can get reviews that haven't been published yet)
    - POST - for everybody
    """
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewSerializer
        elif self.action == "create":
            return SendReviewSerializer

    def get_queryset(self):
        if self.action == 'list':
            self.search_fields = ['id', 'text']  # TODO: search on 'item_id'
            if self.request.user.is_superuser:
                queryset = Review.objects.order_by('pk').all().select_related('item')
            else:
                queryset = Review.objects.filter(is_published=True).order_by('pk').all().select_related('item')

        elif self.action == 'create':
            queryset = Review.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        review = super().create(request, *args, **kwargs)
        context = {
            'author': review.data['author'],
            'email': review.data['email'],
            'item': review.data['item'],
            'review': review.data['text']
        }
        sendmail.delay(
            template_id='ReviewForAdmin',
            context=context,
            mailto=review.data['email'],
            subject=f"Новый отзыв на товар {review.data['item']}"
        )
        return review
