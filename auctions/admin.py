from django.contrib import admin
from .models import AuctionList, Bid, Comment

admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(Comment)
