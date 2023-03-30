from django.contrib import admin
from django.db.models import Avg

from .models import (
    Comment, Review, Category,
    Title, Genre, GenreTitle)


admin.site.register(Review)
admin.site.register(Comment)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    search_fields = ('name',)


class GenreInline(admin.TabularInline):
    """Инлайн для работы с жанрами произведения в админке."""
    model = GenreTitle
    extra = 2


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'rating',
    )
    inlines = (
        GenreInline,
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)

    def get_rating(self, object):
        """Вычисляет рейтинг произведения."""
        rating = object.reviews.aggregate(average_score=Avg('score'))
        return round(rating.get('average_score'), 1)

    get_rating.short_description = 'Рейтинг'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title',
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('genre',)

