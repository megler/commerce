from itertools import product
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField, IntegerField, DecimalField


class User(AbstractUser):
    """User class returns username, first/last name, password"""

    auctionlist = models.ManyToManyField("ListAuction",
                                         related_name="auctions")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    """Returns auction categories"""

    AUCTION_CATEGORIES = (("Brooms", "Brooms"), ("Wands", "Wands"), ("Capes",
                                                                     "Capes"))
    cat_name = models.CharField(max_length=50,
                                choices=AUCTION_CATEGORIES,
                                default="Brooms")

    categorylist = models.ManyToManyField("ListAuction",
                                          related_name="auction_categories")

    def __str__(self):
        return f"{self.cat_name}"


class ListAuction(models.Model):
    """Allows user to list item for sale"""

    seller = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name="seller")

    CONDITION = (("New", "New"), ("Used", "Used"), ("Refurbished",
                                                    "Refurbished"))

    item_name = models.CharField(max_length=80)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.IntegerField()
    description = models.CharField(max_length=500000)
    item_condition = models.CharField(max_length=30,
                                      choices=CONDITION,
                                      default="New")
    categories = models.ForeignKey(Category,
                                   null=True,
                                   on_delete=models.SET_NULL,
                                   related_name="categories")
    listing_image = models.URLField(null=True)

    def __str__(self):
        return f"Item: {self.item_name}"


class Bid(models.Model):
    """Allows user to bid on auction listing"""

    customer = models.ForeignKey(User,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="user")
    product = models.ForeignKey(
        ListAuction,
        null=True,
        on_delete=models.SET_NULL,
        related_name="auction_item",
    )
    bid = models.IntegerField(null=True)
    high_bidder = models.IntegerField(null=True)  # Will hold ID of high bidder


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
