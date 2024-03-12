from django.contrib import admin
from .models import Bid, Comment, Category, Listing, WonAuction

admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(WonAuction)


