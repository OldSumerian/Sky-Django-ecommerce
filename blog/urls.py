from django.urls import path
from blog.apps import BlogConfig
from blog.models import toggle_publish
from blog.views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blogpost_list"),
    path("blogpost/<int:pk>", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("blogpost/create", BlogPostCreateView.as_view(), name="blogpost_create"),
    path("blogpost/<int:pk>/update", BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("blogpost/<int:pk>/delete", BlogPostDeleteView.as_view(), name="blogpost_delete"),
    path("toggle_publish/<int:pk>", toggle_publish, name="toggle_publish"),
]
