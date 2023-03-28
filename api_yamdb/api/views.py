from content.models import *
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import ( 
    IsAuthenticatedOrReadOnly, SAFE_METHODS)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ( 
    TitleSerializer, CategorySerializer, GenreSerializer, TitleWriteSerializer, TitleReadSerializer) 
from django.db.models import Avg
from .filters import TitleFilter


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Дженерик для операций retrieve/create/list."""

    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet): 
    queryset = Title.objects.all() 
    serializer_class = TitleSerializer 
    pagination_class = LimitOffsetPagination 
    permission_classes = (IsAuthenticatedOrReadOnly,) 


class CategoryViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        # IsAdminOrReadOnly,
    )

class GenreViewSet(CreateListDestroyViewSet):
    """Вьюсет для модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        # IsAdminOrReadOnly,
    )


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Title."""
    queryset = Title.objects.all()
    
    # queryset = Title.objects.annotate(
    #     rating=Avg('reviews__score'),
    # ).order_by('name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        # IsAdminOrReadOnly,
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TitleReadSerializer
        return TitleWriteSerializer
