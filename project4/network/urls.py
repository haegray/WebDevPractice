

from . import views

from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("posts/<int:post_id>", views.posts, name="posts"),
    path("<str:which>", views.index, name="index")
] 
