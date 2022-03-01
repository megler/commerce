from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, ListAuction, Bid, Watchlist
from auctions.forms import ListAuctionForm


def index(request):
    return render(request, "auctions/index.html",
                  {"active_listings": ListAuction.objects.all()})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(request, "auctions/register.html",
                          {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
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

    return render(
        request,
        "auctions/listings-by-cat.html",
        {
            "category": cat,
            "listings":
            ListAuction.objects.all().filter(categories__in=get_cat),
        },
    )


@login_required(login_url="login")
def create_listing(request):
    """ Allow logged in user to create a new listing """

    # Credit: https://forum.djangoproject.com/t/automatically-get-user-id-to-assignate-to-form-when-submitting/5333/6

    form = ListAuctionForm(user=request.user)

    if request.method == "POST":
        form = ListAuctionForm(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.seller = User.objects.get(pk=request.user.id)
            obj.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            print("ERROR : Form is invalid")
            print(form.errors)
    context = {"form": form}
    return render(request, "auctions/create-listing.html", context)
