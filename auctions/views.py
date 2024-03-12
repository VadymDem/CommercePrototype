from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Watchlist
from .models import Category, Listing
from .models import User
from .models import ListingForm


def index(request):
    listings = Listing.objects.all()
    return render(request, 'auctions/index.html', {'listings': listings})


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


def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    categories = Category.objects.all()
    return render(request, 'auctions/create_listing.html', {'form': form, 'categories': categories})


def listing_detail(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, 'auctions/listing_detail.html', {'listing': listing})


def watchlist(request):
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    context = {'watchlist': watchlist}
    return render(request, 'auctions/watchlist.html', context)

@login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.listings.add(listing)
    return redirect('watchlist')

@login_required
def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = Watchlist.objects.get(user=request.user)
    watchlist.listings.remove(listing)
    return redirect('watchlist')


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'auctions/category_list.html', {'categories': categories})


def category_render(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category_render.html', {'category': category, 'listings': listings})
