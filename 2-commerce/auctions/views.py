from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .forms import ListingForm, BidForm, CommentForm
from .models import User, Listing, Bid, Comment, Watchlist

def index(request):
    queryset = Listing.objects.filter(active=True).annotate(current_price=Max('bids__price'))
    categories = Listing.objects.filter(active=True).order_by("category").values_list("category", flat=True).distinct()
    context = {
        'title_end': "- All",
        'object_list': queryset,
        "categories": categories
    }
    return render(request, "auctions/index.html", context)

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

def category_listings(request, category):
    listings = Listing.objects.filter(category=category.upper()).filter(active=True)
    title_end = "- " + category.lower().capitalize()
    categories = Listing.objects.filter(active=True).order_by("category").values_list("category", flat=True).distinct()
    context = {
        "pretitle": title_end,
        "object_list": listings,
        "categories": categories
    }
    return render(request, "auctions/index.html", context)

@login_required
def watchlist(request):
    watchlist = Listing.objects.filter(watchlist__user=request.user)
    watch_count = watchlist.count()
    context = {
        "pretitle": "- Watchlist",
        "object_list": watchlist,
        "watch_count": watch_count
    }
    return render(request, "auctions/index.html", context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            image = form.cleaned_data["image"]
            price = form.cleaned_data["price"]

            listing = Listing(user=request.user, title=title, description=description, category=category, image=image, price=price)
            listing.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        form = ListingForm()

    return render(request, "auctions/create.html", {'form': form})

def listing_view(request, id):
    item = Listing.objects.get(id=id)
    comments = Comment.objects.filter(listing=id)
    current_price = current_price_func(request, item)
    watched = watch_func(request, id)
    bid_count=Bid.objects.filter(listing=id).count()

    if request.method == 'POST':
        if "watch" in request.POST:
            watch = Watchlist(user=request.user, listing=item)
            watch.save()
            return HttpResponseRedirect(reverse("listing_detail", args=(str(id))))

        if "unwatch" in request.POST:
            watched_item = Watchlist.objects.get(user=request.user, listing=item)
            watched_item.delete()
            return HttpResponseRedirect(reverse("listing_detail", args=(str(id))))
        
        if "end_auction" in request.POST:
            end_auction(request, item)

        if "post_comment" in request.POST:
            com_form = CommentForm(request.POST)
            if com_form.is_valid():
                com_content = com_form.cleaned_data["comment"]
                comment = Comment(user=request.user, listing=item, comment=com_content)
                comment.save()
                return HttpResponseRedirect(reverse("listing_detail", args=(str(id))))
        else:
            com_form = CommentForm()

        if "place_bid" in request.POST:
            bid_form = BidForm(request.POST, listing=item)
            if bid_form.is_valid():
                bid_price = bid_form.cleaned_data["price"]
                bid = Bid(user=request.user, listing=item, price=bid_price)
                bid.save()
                return HttpResponseRedirect(reverse("listing_detail", args=(str(id))))
        else :
            bid_form = BidForm()

        context = {
            'item': item,
            'bid_form': bid_form,
            'comments': comments,
            'com_form': com_form,
            'watching': watched,
            'current_price': current_price,
            'bid_count': bid_count,
        }

        return render(request, "auctions/listing.html", context)
    
    context = {
        'item': item,
        'bid_form': BidForm(),
        'comments': comments,
        'com_form': CommentForm(),
        'watching': watched,
        'current_price': current_price,
        'bid_count': bid_count,
    }

    return render(request, "auctions/listing.html", context)

@login_required
def watch_func(request, id):
    if User.is_authenticated:
        watched_item = Watchlist.objects.filter(listing=id, user=request.user)
        if watched_item:
            watched = True
        else:
            watched = False
    return watched

def current_price_func(request, listing):
    all_bids = Bid.objects.filter(listing=listing)
    if all_bids:
        highest_bid = all_bids.order_by("price").last().price
        current_price = highest_bid
    else:
        current_price = listing.price
    return current_price

def end_auction(request, listing):
    winning_bid = Bid.objects.filter(listing=listing).order_by("price").last()
    if winning_bid:
        listing.purchaser = winning_bid.user
    listing.active = False
    listing.save()

    return HttpResponseRedirect(reverse("listing_detail", args=(str(listing.id))))
