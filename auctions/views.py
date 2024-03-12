from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Watchlist
from .models import Category, Listing, WonAuction, Bid, Comment
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


@login_required  # Декоратор, чтобы проверить, что пользователь аутентифицирован
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            # Получаем текущего пользователя
            owner = request.user
            # Присваиваем текущего пользователя как владельца объявления
            listing = form.save(commit=False)
            listing.owner = owner
            listing.save()
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


@login_required
def place_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        if bid_amount:
            bid_amount = float(bid_amount)
            if bid_amount > listing.current_price:  # Ensure bid is higher than current price
                bid = Bid(listing=listing, user=request.user, amount=bid_amount)
                bid.save()
                return redirect('listing_detail', listing_id=listing_id)
            else:
                return render(request, 'auctions/error.html',
                              {'error_message': 'Your bid must be higher than the current price.'})

    return render(request, 'auctions/listing_detail.html', {'listing': listing})


@login_required
def close_auction(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    if request.method == 'POST':
        if request.user == listing.owner:
            winner_bid = listing.bids.order_by('-amount').first()
            if winner_bid:
                winner = winner_bid.user
                winning_bid = winner_bid.amount
            else:
                winner = None
                winning_bid = 0

            if winner:
                won_auction = WonAuction(winner=winner, listing_title=listing.title,
                                         listing_description=listing.description,
                                         listing_start_price=listing.start_price,
                                         listing_image_url=listing.image_url,
                                         winning_bid=winning_bid)
                won_auction.save()

                listing.delete()

                return redirect('index')
            else:
                return HttpResponseForbidden("Auction cannot be closed without a winner.")
        else:
            return render(request, 'auctions/error.html', {'error_message': 'Only the owner can close the auction.'})
    else:
        return render(request, 'auctions/error.html', {'error_message': 'Invalid request method.'})


@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        text = request.POST.get('comment')
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment.objects.create(auction=listing, user=user, text=text)
        comment.save()
    return redirect('listing_detail', listing_id=listing_id)