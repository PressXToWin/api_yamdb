from django.db import models
from users.models import User


class Title(models.Model):
    """Mодель произведения."""
    name = models.CharField(max_length=256, verbose_name='Произведение',
                            help_text='Введите название произведения')

    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание произведения',
        help_text='Введите описание произведения')

    year = models.PositiveIntegerField(
        verbose_name='Год публикации',
        help_text='Укажите год публикации',)

    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        null=True, blank=True,
        default=None)

    category = models.ForeignKey(
        'Category', blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категорию произведения',
        help_text='Выберите категорию по желанию')

    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр',
        through='GenreTitle')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')


class Category(models.Model):
    """Mодель категория."""
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        unique=True,
        help_text='Введите название категории')

    slug = models.SlugField(
        verbose_name='Псевдоним категории',
        max_length=64, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )


class Genre(models.Model):
    """Mодель жанр."""
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
        help_text='Введите название жанра')

    slug = models.SlugField(
        verbose_name='Псевдоним жанра',
        max_length=64, unique=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name', )


class GenreTitle(models.Model):
    """Связь жанра и тайтла."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE)

    genre = models.ForeignKey(
        Genre,
        null=True, blank=True,
        verbose_name='Жанр',
        on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        constraints = (
            models.UniqueConstraint(
                fields=('genre', 'title'),
                name='unique_genre_title',
            ),
        )
