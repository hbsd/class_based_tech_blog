from django.db import models
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
	title = models.CharField(max_length=200)
	author = models.ForeignKey(
		'auth.User',
		on_delete=models.CASCADE,
	)
	body = models.TextField()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.CharField(max_length=140)
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return self.comment

	def get_absolute_url(self):
		return reverse('post_details')
