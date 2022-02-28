from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Bid, Category, ListAuction

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(ListAuction)
