
from django.urls import path, re_path
from django.contrib import admin

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_user_id>", views.profile_view, name="profile-view"),
    path("profile/<int:profile_user_id>/follow", views.profile_follow, name="profile-follow"),
    path("posts/following", views.following_posts_view, name="following-posts-view"),
    path('posts/new', views.post_create, name='post-create'),
    path("posts/<int:post_id>/edit", views.post_edit, name="post-edit"),
    path("posts/<int:post_id>/like", views.post_like, name="post-like"),
    path("profile/<int:profile_user_id>/follow", views.profile_follow, name="profile-follow"),
]
