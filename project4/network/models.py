from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(default="")
    create_time = models.DateTimeField(auto_now=True)


class Follower(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_by")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

