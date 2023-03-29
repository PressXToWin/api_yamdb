from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('С этим именем зарегистрироваться невозможно')
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=149)
    confirmation_code = serializers.CharField(required=True, max_length=36)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User
