from rest_framework import serializers

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'is_staff', 'is_superuser']


class NoticeSerializer(serializers.ModelSerializer):
    publisher = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Notice
        fields = ['id', 'title', 'content', 'edit_time', 'priority', 'publisher']
