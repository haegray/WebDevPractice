from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(upload_to = 'media',null=True, blank=True)
    user_following = models.ManyToManyField('User', blank=True, related_name="following")
    user_followers = models.ManyToManyField('User', blank=True, related_name="followers")

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):

    id = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="posts")
    post = models.CharField(max_length=128)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f" {self.poster}: {self.post} at {self.time_stamp}"

class Like(models.Model):

    id = models.AutoField(primary_key=True)
    liker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    
    def __str__(self):
        return f" {self.liker}: liked {self.post}"


