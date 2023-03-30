from django.shortcuts import get_object_or_404
from models import Review, Title
from permissions import AdminModeratorAuthorPermission
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from serializers import CommentSerializer, ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permisson_classes = (AdminModeratorAuthorPermission,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    permisson_class = (AdminModeratorAuthorPermission,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
