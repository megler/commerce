# CSCI E-33a - Commerce
#
# Assignment 2 - Commerce
# Usage:
#      A Django based auction application.
#
# Marceia Egler March 6, 2022

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Category, ListAuction, Bid, Watchlist, Comment
from auctions.forms import ListAuctionForm
from datetime import timedelta
from . import util


def index(request):
    bids = Bid.objects.all()
    return render(
        request,
        "auctions/index.html",
        {
            "bids": bids,
        },
    )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"].lower(
        )  # remove case sensitivity from login
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(
                request,
                "Invalid username and/or password.",
            )
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"].lower()  # make username lowercase
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(
                request,
                "Passwords must match.",
            )
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(
                request,
                "Username already taken.",
            )
            return render(
                request,
                "auctions/register.html",
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def auction_categories(request):

    return render(
        request,
        "auctions/categories.html",
        {
            "categories": Category.objects.all(),
            "listings": ListAuction.objects.all(),
        },
    )


def active_by_cat(request, cat):
    """Returns active listings by category"""

    # I believe naming convention for HTML page names is hyphen not underscore
    # but Google was sketchy on details and I didn't see what I wanted on MDN.

    # use of __in credit:
    # https://stackoverflow.com/questions/55994907/the-queryset-value-for-an-exact-lookup-must-be-limited-to-one-result-using-slici
    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/

    get_cat = Category.objects.filter(cat_name=cat).values_list("id",
                                                                flat=True)
    listings = ListAuction.objects.all().filter(categories__in=get_cat)
    current_bid = Bid.objects.all().filter(product__in=listings,
                                           high_bidder=True)

    return render(
        request,
        "auctions/listings-by-cat.html",
        {
            "category": cat,
            "listings_with_bid": current_bid,
        },
    )


@login_required(login_url="login")
def create_listing(request):
    """ Allow logged in user to create a new listing """

    # Credit: https://forum.djangoproject.com/t/automatically-get-user-id-to-assignate-to-form-when-submitting/5333/6

    # MSG-TO-TA - I don't know why this needs to be here twice, but the form
    # renders incorrectly if you don't.

    form = ListAuctionForm(user=request.user)

    if request.method == "POST":
        form = ListAuctionForm(request.POST, user=request.user)

        if form.is_valid():
            # Save form submission
            obj = form.save(commit=False)
            obj.seller = User.objects.get(pk=request.user.id)
            obj.save()
            with transaction.atomic():
                # Also push starting bid to bid table
                product_id = ListAuction.objects.get(
                    item_name=form.cleaned_data["item_name"]).id
                bid = ListAuction.objects.get(
                    starting_bid=form.cleaned_data["starting_bid"]
                ).starting_bid
                new_bid = Bid(
                    bid=bid,
                    customer_id=request.user.id,
                    product_id=product_id,
                    high_bidder=True,
                )
                new_bid.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create-listing.html",
                          {"message": form.errors})
    context = {"form": form}
    return render(request, "auctions/create-listing.html", context)


def get_listing(request, title, message=""):
    """Returns single listing by name"""

    get_listing_info = ListAuction.objects.get(item_name=title)
    get_cat = Category.objects.get(pk=get_listing_info.categories_id)
    expire = get_listing_info.date_created + timedelta(days=7)
    current_bid = Bid.objects.get(product_id=get_listing_info.id,
                                  high_bidder=True)
    get_comments = Comment.objects.all().filter(product=get_listing_info.id)

    # Get all items from user's watchlist so you can extract specific prod id's
    verify_watchlist = Watchlist.objects.filter(buyer_id=request.user.id)
    # Get product id's from logged in user's watchlist
    # Credit: https://stackoverflow.com/questions/7054189/checking-if-something-exists-in-items-of-list-variable-in-django-template
    list_id = [i.product_id for i in verify_watchlist]

    return render(
        request,
        "auctions/detail.html",
        {
            "high_bidder": current_bid.customer_id,
            "current_bid": current_bid.bid,
            "expire_date": util.datetime_from_utc_to_local(expire),
            "category": get_cat,
            "item": get_listing_info,
            "message": message,
            "verify_watchlist": list_id,
            "comments": get_comments,
        },
    )


@login_required(login_url="login")
def end_auction(request, id=None):
    """ Allow the user who signed in and is the one who created the listing to end the auction early. """
    listing = ListAuction.objects.get(id=id)
    listing.status = False
    listing.save()
    # Credit: https://stackoverflow.com/questions/2005822/django-forms-reload-view-after-post
    return redirect(request.META["HTTP_REFERER"])


def bid_item(request, title):
    """ Logged in user can bid on an item """
    get_listing_info = ListAuction.objects.get(item_name=title)
    get_bid = (Bid.objects.filter(
        product_id=get_listing_info.id).order_by("-bid")[:1].get())

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to bid.")
            return get_listing(
                request,
                title=title,
            )
        if request.user.is_authenticated and get_listing_info.status:
            bid_amt = float(request.POST["bid-amt"])
            if (bid_amt < get_listing_info.starting_bid
                    and get_bid.bid == get_listing_info.starting_bid):
                messages.error(
                    request,
                    "Your bid needs to be equal to or higher than the starting bid.",
                )
                return get_listing(request, title=title)
            if bid_amt <= get_bid.bid and get_bid.bid > get_listing_info.starting_bid:
                messages.error(
                    request,
                    "Your bid needs to be greater than the current high bid.",
                )
                return get_listing(
                    request,
                    title=title,
                )
            else:
                # remove current high bidder and add new high bidder
                get_bid.high_bidder = False
                get_bid.save()
                with transaction.atomic():
                    Bid.objects.create(
                        bid=bid_amt,
                        customer_id=request.user.id,
                        product_id=get_listing_info.id,
                        high_bidder=True,
                    )
                messages.success(
                    request,
                    "You are now the highest bidder!",
                )
                return get_listing(request, title=title)

    return redirect(request.META["HTTP_REFERER"])


def add_to_watchlist(request, title):
    get_listing_info = ListAuction.objects.get(item_name=title)
    get_bid = Bid.objects.get(product_id=get_listing_info.id, high_bidder=True)
    if request.method == "POST":
        if request.user.is_authenticated:
            p = Watchlist(
                buyer_id=request.user.id,
                product_id=get_listing_info.id,
                bids_id=get_bid.id,
            )
            p.save()
            messages.success(
                request,
                "Item added to watchlist.",
            )
            return get_listing(request, title=title)
        else:
            messages.error(
                request,
                "You must be logged in to have a watchlist.",
            )
            return get_listing(request, title=title)
    return redirect(request.META["HTTP_REFERER"])


@login_required(login_url="login")
def delete_from_watchlist(request, id=None):
    """ Allow logged in user to remove item from watchlist"""

    # Credit: https://stackoverflow.com/questions/44248228/django-how-to-delete-a-object-directly-from-a-button-in-a-table
    object = Watchlist.objects.get(id=id)
    object.delete()
    return redirect(request.META["HTTP_REFERER"])


@login_required(login_url="login")
def show_watchlist(request):
    """ Show logged in user all items in watchlist """
    items = Watchlist.objects.all().filter(buyer=request.user.id)

    return render(request, "auctions/watchlist.html", {"watch_items": items})


def add_comment(request, title, message=""):
    """ Logged in user can add comments to an auction item. """
    get_listing_info = ListAuction.objects.get(item_name=title)
    if request.method == "POST":
        comment = request.POST["comment"]
        if request.user.is_authenticated:
            p = Comment(
                user_id=request.user.id,
                product_id=get_listing_info.id,
                comment=comment,
            )
            p.save()
            return get_listing(request, title=title)
    return redirect(request.META["HTTP_REFERER"])
