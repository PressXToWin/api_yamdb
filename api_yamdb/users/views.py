from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsAdminRole
from users.serializers import SignupSerializer, TokenSerializer, UsersSerializer, ReadonlyRoleSerializer

User = get_user_model()


class APISignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save(confirmation_code=str(uuid4()))
        except IntegrityError:
            try:
                user = User.objects.get(username=request.data['username'], email=request.data['email'])
            except:
                return Response(
                    {'error': 'Такой пользователь уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST)
        send_mail(
            subject='Вы зарегистрированы на YamDB',
            message='Вы зарегистрированы на YamDB \n'
            f'Ваше имя пользователя: {user.username} \n'
            f'Ваш код доступа к API: {user.confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class APITokenView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'error': 'Такого пользователя не существует.'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(
            {'error': 'Неверный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'error': 'Метод не предусмотрен.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        if request.method == 'PATCH':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def user_detail(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = ReadonlyRoleSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
