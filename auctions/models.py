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

    def __str__(self):
        return f"{self.cat_name}"


class AuctionItem(models.Model):
    """Returns specific auction item"""

    CONDITION = (("N", "New"), ("U", "Used"), ("R", "Refurbished"))
    SHIPPING = (
        ("Gr", "Ground"),
        ("Exp", "Express"),
        ("Pr", "Priority"),
        ("Int", "International"),
    )
    listing_image = models.ImageField(
        upload_to="./static/auctions/auction_images")
    item_name = models.CharField(max_length=80)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.IntegerField()
    description = models.CharField(max_length=500000)
    shipping_options = models.CharField(max_length=3,
                                        choices=SHIPPING,
                                        default="Gr")
    item_condition = models.CharField(max_length=1,
                                      choices=CONDITION,
                                      default="N")
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"Item: {self.item_name}\nPrice: {self.price}\nQuantity:{self.quantity}"


class Bid(models.Model):
    """Allows user to bid on auction listing"""

    customer = models.ForeignKey(User,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="user")
    product = models.ForeignKey(
        AuctionItem,
        null=True,
        on_delete=models.SET_NULL,
        related_name="auction_item",
    )


class ListAuction(models.Model):
    """Allows user to list item for sale"""

    seller = models.ForeignKey(User,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name="seller")

    product = models.ForeignKey(
        AuctionItem,
        null=True,
        on_delete=models.SET_NULL,
        related_name="item_to_list",
    )
