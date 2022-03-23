from django.contrib import admin
from .models import User, Listing, Bid, Category, Comments
# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "current_price", "owned_by", "description", "photo")
    
class BidAdmin(admin.ModelAdmin):
    list_filter = ("listed_item",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "icon", "description")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listed_item","time_stamp","commenter", "comment")


admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentAdmin)