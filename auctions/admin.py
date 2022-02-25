from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionItem, Bid, Category, ListAuction
from PIL import Image

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(AuctionItem)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(ListAuction)
