from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.IntegerField(default=0)
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")
    
    
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    ACTIVE = "active"
    INACTIVE = "inactive"
    STATUS = [
        (ACTIVE, "active"),
        (INACTIVE, "inactive"),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    current_price = models.IntegerField(default=0)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    description = models.CharField(max_length=64, default="")
    photo = models.ImageField(upload_to = 'media',null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True, related_name="categories")
    status = models.CharField(max_length=8, choices=STATUS, default=ACTIVE)
    highest_bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="highest_bidder", null=True, blank=True)

    def __str__(self):
        return f"{self.title}: {self.description} Current Price: {self.current_price} Status: {self.status} "

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listed_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_items")
    
    

    def __str__(self):
        return f"Bid {self.id}: {self.bidder} bids {self.bid} on {self.listed_item.title}"

class Category(models.Model):

    HOMEGOODS = "Home Goods"
    TECHNOLOGY = "Technology"
    MKITEMS = "Mario Kart Items"
    DECOR = "Decor"
    MISCELLANEOUS = "Misc"

    CATEGORY = [
        (HOMEGOODS, "Home Goods"),
        (TECHNOLOGY, "Technology"),
        (MKITEMS, "Mario Kart Items"),
        (DECOR, "Decor"),
        (MISCELLANEOUS, "Misc")
    ]


    id = models.AutoField(primary_key=True)
    icon = models.ImageField(upload_to = 'media',null=True, blank=True)
    title = models.CharField(max_length=64, choices=CATEGORY, default=MISCELLANEOUS)
    description = models.CharField(max_length=64)

    def __str__(self):
        return f" {self.title}"
