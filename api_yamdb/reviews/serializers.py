from rest_framework import serializers
from reviews.models import *
import re
from django.utils import timezone
from django.shortcuts import get_object_or_404

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""
    def validate_slug(self, value):
        """Проверка соответствия слага категории."""
        if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Псевдоним категории не соотвествует формату',
            )
        return value

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""

    def validate_slug(self, value):
        """Проверка соответствия слага жанра."""
        if not re.fullmatch(r'^[-a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                'Псевдоним жанра не соотвествует формату',
            )
        return value

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class RatingRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.score

class TitleSerializer(serializers.ModelSerializer):
    """Базовый сериализатор модели Title."""

    # rating = serializers.IntegerField(read_only=True)
    rating = RatingRelatedField(read_only=True)

    def validate_year(self, value):
        """Проверка года на будущее время."""
        current_year = timezone.now().year
        if value > current_year:
            raise serializers.ValidationError(
                'Марти, ты опять взял Делориан без спроса?!',
            )
        return value

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class TitleReadSerializer(TitleSerializer):
    """Сериализатор модели Title для чтения."""
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)


class TitleWriteSerializer(TitleSerializer):
    """Сериализатор модели Title для записи."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False,
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_data',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    title = serializers.SlugRelatedField(
        read_only=True, slug_field='name')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'title')
        model = Review

    def validate_score(self, value):
        if not 0 < value < 11:
            raise serializers.ValidationError('Оценка по 10 бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Review.objects.filter(
                title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв к этому произведению!'
            )
        return data
