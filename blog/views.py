from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .forms import CommentForm

from .models import Post

from taggit.models import Tag


class BlogListView(ListView):
	model = Post
	template_name = 'tech_index.html'
	paginate_by = 4


class BlogDetailView(DetailView, View):
	model = Post
	template_name = 'tech_single.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()
		return context

	def get(self, request, *args, **kwargs):
		view = CommentGet.as_view()
		return view(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		view = CommentPost.as_view()
		return view(request, *args, **kwargs)


class BlogCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'post_new.html'
	fields = ['title_image', 'title', 'body', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	template_name = 'post_edit.html'
	fields = ['title_image', 'slug', 'title', 'body', 'tags']

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('tech_index')

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class CommentGet(DetailView):
	model = Post
	template_name = 'tech_single.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()
		return context


class CommentPost(SingleObjectMixin, FormView):
	model = Post
	form_class = CommentForm
	template_name = 'tech_single.html'

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().post(request, *args, **kwargs)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.post = self.object
		comment.save()
		return super().form_valid(form)

	def get_success_url(self):
		post =  self.get_object()
		return reverse('tech_single', kwargs={'slug': post.slug})


class SearchResultsView(ListView):
	model = Post
	template_name = 'search_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q')
		object_list = Post.objects.filter(
			Q(title__icontains=query) | Q(body__icontains=query)
		)
		return object_list
