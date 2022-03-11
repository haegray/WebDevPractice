from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.IntegerField(default=0)
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist")
    
    
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    current_price = models.IntegerField(default=0)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    description = models.CharField(max_length=64, default="")
    photo = models.ImageField(upload_to = 'media',null=True, blank=True)
    category = models.ManyToManyField('Category', blank=True, related_name="categories")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: {self.description} Current Price: {self.current_price} "

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid = models.IntegerField(default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listed_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_items")
    
    

    def __str__(self):
        return f"<Bid {self.id}: {self.bidder} bids {self.bid} on {self.listed_item.title}"

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    icon = models.ImageField(upload_to = 'media',null=True, blank=True)
    title = models.CharField(max_length=64, default='General')
    description = models.CharField(max_length=64)
