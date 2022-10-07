from django.contrib.auth.mixins import (
	LoginRequiredMixin,
	UserPassesTestMixin
)
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
from django.urls import reverse_lazy, reverse

from .forms import CommentForm

from .models import Post


class BlogListView(ListView):
	model = Post
	template_name = 'home.html'
	paginate_by = 2


class BlogDetailView(DetailView, View):
	model = Post
	template_name = 'post_detail.html'

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
	fields = ['title_image', 'title', 'body']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	template_name = 'post_edit.html'
	fields = ['title_image', 'slug', 'title', 'body']

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'post_delete.html'
	success_url = reverse_lazy('home')

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class CommentGet(DetailView):
	model = Post
	template_name = 'post_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = CommentForm()
		return context


class CommentPost(SingleObjectMixin, FormView):
	model = Post
	form_class = CommentForm
	template_name = 'post_detail.html'

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
		return reverse('post_detail', kwargs={'slug': post.slug})
