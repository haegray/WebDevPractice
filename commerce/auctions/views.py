from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid


def index(request):

    listings = Listing.objects.all()
    #names = [listing.title for listing in listings]
    #images = [listing.photo for listing in listings]
    #bids = [listing.bids.all() for listing in listings]
    #values = zip(names,bids)
    #function that fills the lists.
    
    #context = {'listings': values }

    return render(request, "auctions/index.html", {
        "listings": listings
    })

def listing(request, title):
    listing = Listing.objects.get(title = title)
    bids = [bid for bid in listing.bids.all()]
   
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids
    })

def add_listing(request):
    if request.method == "POST":
        try:
            listing = Listing.objects.get(title = request.POST.get('title'))
            return HttpResponseNotFound("This item already exists.")
        except Listing.DoesNotExist:
            title = request.POST.get('title')
            current_price = request.POST.get('current_price')
            owned_by = User.objects.get(username = request.POST.get('owned_by'))
            print("request user ", request.user)
            print("owned by", owned_by)
            if str(request.user) != str(owned_by):
                return HttpResponseNotFound("You can only post your own listing.")
            description = request.POST.get('description')
            photo = request.FILES.get('photo')
            l = Listing(title=title, current_price=current_price, owned_by=owned_by, description=description, photo=photo)
            l.save()
            listings = Listing.objects.all()
            return render(request, "auctions/index.html", {
            "listings": listings
            })
    else:
        return render(request, "auctions/add_listing.html")
    


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
