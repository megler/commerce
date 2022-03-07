from itertools import product
from re import L
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from . import util


class User(AbstractUser):
    """User class returns username, first/last name, password"""

    auctionlist = models.ManyToManyField("ListAuction",
                                         related_name="auctions")

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    """Returns auction categories"""

    cat_name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.cat_name}"


class ListAuction(models.Model):
    """Allows user to list item for sale"""

    seller = models.ForeignKey(User,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name="seller")

    CONDITION = (("New", "New"), ("Used", "Used"), ("Refurbished",
                                                    "Refurbished"))
    date_created = models.DateTimeField(auto_now_add=True)
    item_name = models.CharField(max_length=80)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.IntegerField()
    description = models.CharField(max_length=500000)
    item_condition = models.CharField(max_length=30,
                                      choices=CONDITION,
                                      default="New")
    categories = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="categories",
    )
    listing_image = models.URLField(null=True, blank=True)
    # status True is Active. False is Inactive
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Item: {self.item_name}"


class Bid(models.Model):
    """Allows user to bid on auction listing"""

    customer = models.ForeignKey(User,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name="user")
    product = models.ForeignKey(
        ListAuction,
        null=True,
        on_delete=models.CASCADE,
        related_name="auction_item",
    )
    bid = models.DecimalField(decimal_places=2, max_digits=7)
    high_bidder = models.BooleanField(
        default=True)  # Will hold ID of high bidder

    def __str__(self):
        return f"Item Bid: {self.product.item_name}"


class Watchlist(models.Model):
    """Allows user to add or delete item from watchlist"""

    buyer = models.ForeignKey(User,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name="buyer")

    product = models.ForeignKey(
        ListAuction,
        null=True,
        on_delete=models.SET_NULL,
        related_name="item_to_watch",
    )

    bids = models.ForeignKey(
        Bid,
        null=True,
        on_delete=models.SET_NULL,
        related_name="bids",
    )

    def __str__(self):
        return f"User: {self.buyer.username} | Item: {self.product.item_name}"


class Comment(models.Model):
    user = models.ForeignKey(User,
                             null=True,
                             on_delete=models.SET_NULL,
                             related_name="commenter")

    product = models.ForeignKey(
        ListAuction,
        null=True,
        on_delete=models.SET_NULL,
        related_name="item_to_comment",
    )

    comment = models.CharField(max_length=500000)

    def __str__(self):
        return f"Comment by User: {self.user.username} | Item: {self.product.item_name}"


# Receivers
@receiver(post_save, sender=ListAuction)
def my_handler(sender, **kwargs):
    get_user = sender.objects.latest("id").seller.id
    get_product = sender.objects.latest("id").id
    get_bid = sender.objects.latest("id").starting_bid

    sender.model = Bid.objects.create(
        customer=User.objects.get(id=get_user),
        product=sender.objects.get(id=get_product),
        bid=get_bid,
        high_bidder=True,
    )
