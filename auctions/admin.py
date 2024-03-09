from django.contrib import admin
from .models import AuctionList, Bid, Comment, Category, Listing

admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Category)
