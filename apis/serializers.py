from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
	class Meta:
		fields = (
			'id',
			'author',
			'title',
			'body',
			'created',
		)
		model = Post


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = get_user_model()
		fields = ('id', 'username',)
