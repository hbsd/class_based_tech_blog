from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):
	model = Comment
	extra = 0


class PostAdmin(admin.ModelAdmin):
	inlines = [
		CommentInline,
	]
	list_display = ['title', 'author', 'publish', 'status']
	list_filter = ['status', 'created', 'publish', 'author']
	search_fields = ['title', 'body']
	raw_id_fields = ['author']
	date_hierarchy = 'publish'
	ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
