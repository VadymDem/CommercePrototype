from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.current_price:
            self.current_price = self.start_price
        super().save(*args, **kwargs)

    def update_current_price(self):
        highest_bid = self.bids.order_by('-amount').first()
        if highest_bid:
            self.current_price = highest_bid.amount
            self.save()


class Bid(models.Model):
    listing = models.ForeignKey(Listing, related_name='bids', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.listing.update_current_price()

    def __str__(self):
        return f"Bid by {self.user.username} on {self.listing.title} for ${self.amount}"


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_price', 'image_url', 'category']


class AuctionList(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Comment(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)


class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField('Listing', blank=True)

    def __str__(self):
        return f"Watchlist for {self.user.username}"


