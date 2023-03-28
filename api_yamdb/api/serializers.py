from rest_framework import serializers 
from content.models import *
from rest_framework.validators import UniqueTogetherValidator 


class TitleSerializer(serializers.ModelSerializer): 
 
    class Meta: 
        model = Title 
        fields = '__all__' 
