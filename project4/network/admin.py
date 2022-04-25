from django.contrib import admin
from .models import User, Post, Like
# Register your models here.

class UserAdminAdmin(admin.ModelAdmin):
    list_display = ("id", "photo", "user_following", "user_followers")
    
class PostAdmin(admin.ModelAdmin):
    list_filter = ("id", "poster", "post", "time_stamp")

class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "liker", "post")



admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)