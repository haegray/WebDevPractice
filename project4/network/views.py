from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.forms import ModelForm
from django import forms
import datetime

from .models import User, Post, Like
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage

class PostForm(ModelForm):
    post = forms.CharField(widget=forms.Textarea)
    class Meta:
        # write the name of models for which the form is made
        model = Post   
 
        # Custom fields
        fields = '__all__'
        widgets = {
            'poster': forms.HiddenInput()
        }
 
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user', None)
         super(PostForm, self).__init__(*args, **kwargs)

    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(PostForm, self).clean()
         
        # extract the username and text field from the data
        self.cleaned_data['poster'] = self.user
        
        post = self.cleaned_data.get('post')
        if len(post) > 128:
            self._errors['post'] = self.error_class([
                'Post cannot be longer than 128 characters.' 
            ])
        time_stamp = datetime.datetime.now()
        return self.cleaned_data


def index(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
        print(form.is_valid())
        print(form.errors)

    p = []
    print("Request user id is ", request.user.id)
    if request.user.id != None:
        user = User.objects.get(username = request.user)
        feed_following = user.following
        feed = [Post.objects.filter(poster=user) for user in feed_following.all()] + list(Post.objects.filter(poster=request.user))
        p = Paginator(feed, 2)
        feed = p.get_page(1)
        print("feed ", feed)
        print("p", p)
        
    return render(request, "network/index.html", {
        "feed": feed,
        "form": form
    })

def profile_view(request):
   return render(request, "network/profile.html") 

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        photo = request.FILES["img"]

        fs = FileSystemStorage()
        filename = fs.save(photo.name, photo)
        photo_url = fs.url(filename)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.photo = filename
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
