from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.products.models import ImageColorItem
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer, SendReviewSerializer

# Create your views here.


class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    API endpoint for reviews - /api/v1/reviews/
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
                queryset = Review.objects.order_by('pk').all()  # .select_related('item')
            else:
                # .order_by('pk').all()  # .select_related('item')
                queryset = Review.objects.filter(is_published=True).order_by('pk').all()

        elif self.action == 'create':
            queryset = Review.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()(data=request.data)
        if serializer_class.is_valid():
            data = dict(request.data)
            item_id = data['item']
            image_review = data.get('image', None)
            if image_review is None:
                main_image = ImageColorItem.objects.filter(
                    item_id=item_id,
                    is_main_image=True,
                    color_id=ImageColorItem.objects.filter(item_id=item_id,
                                                           is_main_color=True).values('color_id').get()["color_id"]
                ).values().first()
                image_review = main_image['image']
                serializer_class.save(image=image_review)

                # context = {
                #     'author': review.data['author'],
                #     'email': review.data['email'],
                #     'item': review.data['item'],
                #     'review': review.data['text']
                # }
                # sendmail.delay(
                #     template_id='ReviewForAdmin',
                #     context=context,
                #     mailto=review.data['email'],
                #     subject=f"Новый отзыв на товар {review.data['item']}"
                # )

                return Response(serializer_class.data)
