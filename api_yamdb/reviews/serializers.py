from django.shortcut import get_object_or_404
from models import Comment, Reviews, Title
from rest_fromework import serializers


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
        fields = ('id', 'text', 'author', 'score', 'pub_data')
        model = Reviews

    def validate_score(self, value):
        if not 0 < value < 11:
            raise serializers.ValidationError('Оценка по 10 бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST' and Reviews.objects.filter(
                title=title, author=author).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв к этому произведению!'
            )
        return data
