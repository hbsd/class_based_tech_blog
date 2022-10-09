from django.urls import path
from .views import (
	BlogListView,
	BlogDetailView,
	BlogCreateView,
	BlogUpdateView,
	BlogDeleteView,
	SearchResultsView,
)

urlpatterns = [
	path('post/new/', BlogCreateView.as_view(), name='post_new'),
	path('post/<slug:slug>/', BlogDetailView.as_view(), name='tech_single'),
	path('post/<slug:slug>/edit/', BlogUpdateView.as_view(), name='post_edit'),
	path('post/<slug:slug>/delete/', BlogDeleteView.as_view(), name='post_delete'),
	path('search/', SearchResultsView.as_view(), name='search_results'),
	path('', BlogListView.as_view(), name='tech_index'),
]
