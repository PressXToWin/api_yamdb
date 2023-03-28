from content.models import *
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import ( 
    IsAuthenticatedOrReadOnly, IsAuthenticated)
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ( 
    TitleSerializer,) 


class TotleViewSet(viewsets.ModelViewSet): 
    queryset = Title.objects.all() 
    serializer_class = TitleSerializer 
    pagination_class = LimitOffsetPagination 
    permission_classes = (IsAuthenticatedOrReadOnly,) 
