from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse

from django.forms import ModelForm
from django import forms


from .models import User, Listing, Bid, Category

ACTIVE = "active"
INACTIVE = "inactive"
STATUS = [
    (ACTIVE, "active"),
    (INACTIVE, "inactive"),
]

class ListingForm(ModelForm):
    class Meta:
        # write the name of models for which the form is made
        model = Listing      
 
        # Custom fields
        fields = ["title", "current_price", "owned_by", "description", "photo", "category"]
 
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(ListingForm, self).__init__(*args, **kwargs)

    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(ListingForm, self).clean()
         
        # extract the username and text field from the data
        title = self.cleaned_data.get('title')
        current_price = self.cleaned_data.get('current_price')
        owned_by = self.cleaned_data.get('owned_by')

 
        # conditions to be met for the username length
        print(title)
        if len(title) < 1:
            self._errors['username'] = self.error_class([
                'Minimum 1 character required'])
        print(current_price)
        if current_price <1:
            self._errors['current_price'] = self.error_class([
                'Price must be above 0'])
        if str(self.user) != str(owned_by):
                self._errors['owned_by'] = self.error_class([
                "You can only post your own listing."])
        if title == 'watchlist':
                self._errors['title'] = self.error_class([
                "Forbidden title."])
        print(self.cleaned_data)
        # return any errors if found
        return self.cleaned_data

class BidForm(ModelForm):
    
    class Meta:
        # write the name of models for which the form is made
        model = Bid    
        fields = '__all__'
        widgets = {
            'bidder': forms.HiddenInput(), "listed_item": forms.HiddenInput()
        }
        # Custom fields


    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user', None)
         self.listed_item = kwargs.pop('listed_item', None)
         super(BidForm, self).__init__(*args, **kwargs)
         #self.fields['bidder'].queryset = user
         #self.fields['listed_item'] = listing
    # this function will be used for the validation
    def clean(self):
 
        # data from the form is fetched using super function
        super(BidForm, self).clean()
         
        # extract the username and text field from the data
        
        self.cleaned_data['bidder'] = self.user
        del self._errors['bidder']

        self.cleaned_data['listed_item'] = self.listed_item
        del self._errors['listed_item']

        # conditions to be met for the username length
        if self.cleaned_data['bid'] < self.listed_item.current_price:
            self._errors['bid'] = self.error_class([
                'Bid must be above current price.'])

        if self.listed_item.bid_items.filter(bid=self.cleaned_data['bid'], bidder=self.cleaned_data['bidder']).exists():
            self._errors['bid'] = self.error_class([
                'Cannot make the same bid on one listing.' 
            ])

        if self.user.balance < self.cleaned_data['bid']:
            self._errors['bid'] = self.error_class([
                'Cannot bid above balance.'])

        print(self.cleaned_data)
        print(self.errors)
        # return any errors if found
        return self.cleaned_data

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def categories(request, title):
    print("Title is ", title)
    if title != 'all':
        listings = Listing.objects.filter(category__title = title)
        return render(request, "auctions/index.html", {
        "listings": listings
    })
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def listing(request, title, status):
    listing = Listing.objects.get(title = title)
    user = User.objects.get(username = request.user.username)
    bids = Bid.objects.filter(listed_item=listing)
    
    if user.watchlist.filter(title=listing.title).exists():
        flag = True
    else:
        flag = False

    print("Listing status: ", listing.get_status_display())
    print("Status: ", status)
    if listing.status ==  'active' and status == 'inactive':
        print("Hello is it me you're looking for?")
        listing.status = status
        listing.save()
        print("Listing ", listing)
    else:
        
        if request.method == "POST":
            form = BidForm(request.POST, user=user, listed_item=listing)

            if form.is_valid():
                bid = form.cleaned_data['bid']
                instance = form.save(commit=False)
                instance.bidder = request.user
                instance.listed_item = listing
                instance.save()

                listing.current_price = bid
                listing.highest_bidder = request.user
                listing.save()
                return render(request, "auctions/listing.html", {
                    "form": BidForm(user=request.user, listed_item = listing),
                    "listing": listing,
                    "bids": bids,
                    "current_user": User.objects.get(username=request.user.username),
                    "flag": flag,
                    "status": listing.status
                })
            else:
                return render(request, "auctions/listing.html", {
                    "form": form,
                    "listing": listing,
                    "bids": bids,
                    "current_user": request.user,
                    "flag": flag,
                    "status": listing.status
                })
    return render(request, "auctions/listing.html", {
        "form": BidForm(user=request.user, listed_item = listing),
        "listing": listing,
        "bids": bids,
        "current_user": User.objects.get(username=request.user.username),
        "flag": flag,
        "status": listing.status
    })

def watchlist(request, title):
    current_user = User.objects.get(username = request.user.username)

    if(title != 'watchlist'): 
        listing = Listing.objects.get(title=title)
        if current_user.watchlist.filter(title=listing.title).exists():
            current_user.watchlist.remove(listing)
        else:
            current_user.watchlist.add(listing)
    watchlist = []
    for item in current_user.watchlist.all():
        watchlist.append((item, item.bid_items.all().filter(bidder=current_user)))
    return render(request, "auctions/watchlist.html",{
            "watchlist": watchlist,

        })


def add_listing(request):
    if request.method == "POST":

            form = ListingForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                print("Hello")
                title = form.cleaned_data['title']
                if Listing.objects.filter(title=title).exists():
                    return HttpResponseNotFound("This listing already exists.")
                else:
                    form.save()
                    listings = Listing.objects.all()
                return render(request, "auctions/index.html", {
                "listings": listings
                })
            else:
                return render(request, "auctions/add_listing.html",{
                "form": form
            })
    else:
        return render(request, "auctions/add_listing.html",{
            "form": ListingForm()
        })

    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        print("Username ", username)
        password = request.POST["password"]
        print("Password ", password)
        user = authenticate(request, username=username, password=password)
        print("User is ", user)
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
