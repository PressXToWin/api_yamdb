from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь')
    ]
    bio = models.TextField(
        'Биография',
        blank=True
    )
    role = models.CharField(
        max_length=9,
        choices=ROLES,
        default='user',
    )