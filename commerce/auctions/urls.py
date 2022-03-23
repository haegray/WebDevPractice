from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("watchlist/<str:title>", views.watchlist, name="watchlist"), 
    path('watchlist', views.watchlist, name='watchlist'), 
    path("categories/<str:title>", views.categories, name="categories"),
    path("categories", views.listing, name="categories"),
    path("comment/<str:title>", views.comment, name="comment"),
    path("<str:title>/<str:status>", views.listing, name="listing"),
    path("<str:title>", views.listing, name="listing")
    
]

