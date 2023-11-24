from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post",views.post, name="post"),
    path('admin/', admin.site.urls),
    path("profile/<str:name>", views.profile, name="profile"),
    path("profile/<str:name>/follow", views.manage_follow, name="follow"),
    path("following/", views.following, name="following"),

    # API rountes
    path("posts/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("profile/posts/<int:post_id>/edit/", views.edit_post, name="profile_edit_post"),

    path("posts/<int:post_id>/like/", views.manage_like_post, name="like_post"),
    path("profile/posts/<int:post_id>/like/", views.manage_like_post, name="profile_like_post"),
    path("following/posts/<int:post_id>/like/", views.manage_like_post, name="following_like_post"),

    path("posts/<int:post_id>/comment/", views.manage_comment_post, name="comment_post"),
    path("profile/posts/<int:post_id>/comment/", views.manage_comment_post, name="profile_comment_post"),
    path("following_posts/<int:post_id>/comment/", views.manage_comment_post, name="following_comment_post"),

]
