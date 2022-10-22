from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager


class Post(models.Model):

	class Status(models.TextChoices):
		DRAFT = 'DF', 'Draft'
		PUBLISHED = 'PB', 'Published'

	title = models.CharField(max_length=200, blank=False, null=False)
	slug = models.SlugField(max_length=250, null=False, unique=True)
	title_image = models.ImageField(upload_to='title_image/', blank=False)
	author = models.ForeignKey(
		'auth.User',
		on_delete=models.CASCADE,
	)
	body = models.TextField(blank=False, null=False)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=2,
							  choices=Status.choices,
							  default=Status.PUBLISHED)
	tags = TaggableManager()

	class Meta:
		ordering = ['-publish']
		indexes = [
			models.Index(fields=['-publish']),
		]

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('tech_single', kwargs={'slug': self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)


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
		return reverse('tech_single')
