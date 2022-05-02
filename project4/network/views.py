from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.forms import ModelForm, Textarea
from django import forms
import datetime
import json

from .models import User, Post, Like
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

class PostForm(ModelForm):
    post = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        # write the name of models for which the form is made
        model = Post   
 
        # Custom fields
        fields = '__all__'
        widgets = {
            'poster': forms.HiddenInput(),
            'num_likes': forms.HiddenInput()
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
        if post is None or len(post) > 128:
            self._errors['post'] = self.error_class([
                'Post cannot be longer than 128 characters.' 
            ])
        time_stamp = datetime.datetime.now()
        return self.cleaned_data


def index(request, which=''):
    form = PostForm()
    feed = []
    num_followers = 0
    if request.method == "POST":
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
        form = PostForm()
        return HttpResponseRedirect(reverse("index"))

    if request.user.id != None:
        user = User.objects.get(username = request.user)
        feed_following = user.following
        feed = [post for post in Post.objects.all()]
        print("Which is ", which)
        if which == 'following':
            following = [User.objects.filter(username=ft) for ft in user.following.all()]
            print("Following", following)
            if len(following):
                feed = [post for post in feed if post.poster in following[0].all()]
            else:
                feed = []
        feed = sorted(feed, key=lambda x: x.time_stamp, reverse=True)
        feed_likes = [Like.objects.filter(post=post, liker=request.user).exists() for post in feed]
        feed = list(zip(feed, feed_likes))

        p = Paginator(feed, 4)
        page_number = request.GET.get('page')
        feed = p.get_page(page_number)
        num_followers = len(request.user.followers.all())
        
    return render(request, "network/index.html", {
        "feed": feed,
        "form": form,
        "num_followers": num_followers,
        "current_user": request.user
    })

@csrf_exempt
@login_required
def profile(request, profile):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("profile") is not None:
            f_user = User.objects.get(username=profile)
            if User.objects.get(username=request.user).following.filter(username=profile).exists():
                User.objects.get(username=request.user).following.remove(f_user)
                User.objects.get(username=request.user).save()
                User.objects.get(username=profile).followers.remove(request.user)
                User.objects.get(username=profile).save()
                following = 'Follow'
            else:
                User.objects.get(username=request.user).following.add(f_user)
                User.objects.get(username=request.user).save()
                User.objects.get(username=profile).followers.add(request.user)
                User.objects.get(username=profile).save()
                following = 'Unfollow'
                
        return JsonResponse({
            "num_followers": len(f_user.followers.all()),
            "following": following
        }, safe=False)

    if User.objects.filter(username = profile).exists():
        user = User.objects.get(username = profile)
        feed = list(Post.objects.filter(poster=user))
        feed = sorted(feed, key=lambda x: x.time_stamp, reverse=True)
        feed_likes = [Like.objects.filter(post=post, liker=request.user).exists() for post in feed]
        feed = list(zip(feed, feed_likes))

        following = User.objects.get(username=request.user).following.filter(username=profile).exists()
        if following:
            following = "Unfollow"
        else:
            following = "Follow"

        p = Paginator(feed, 4)
        page_number = request.GET.get('page')
        feed = p.get_page(page_number)
        
    return render(request, "network/profile.html", {
        "feed": feed,
        "current_user": user,
        "num_followers": len(user.followers.all()),
        "following": following
    })

@csrf_exempt
@login_required
def posts(request, post_id):
    print("Post id ", post_id)
    # Query for requested email
    try:
        post = Post.objects.get(id=post_id)
        print("Blah")
    except Post.DoesNotExist:
        print("orange")
        return JsonResponse({"error": "Post not found."}, status=404)
    # change likes on post
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("like") is not None:
            print("Liked")
            try:
                like = Like.objects.get(liker=request.user, post = post)
                print("delete")
                like.delete()
                post.num_likes -= 1
                post.save()
            except Like.DoesNotExist:
                new_like = Like(liker=request.user, post=post)
                new_like.save()
                post.num_likes += 1
                post.save()
                print("saved")
        return JsonResponse({
            "likes": post.num_likes
        }, safe=False)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


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
