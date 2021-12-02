from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.reviews.models import Review
from apps.reviews.serializers import ReviewSerializer, SendReviewSerializer
from apps.email.tasks import sendmail

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
