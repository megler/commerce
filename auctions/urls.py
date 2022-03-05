from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.auction_categories, name="auction_categories"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("bid_item/<str:title>", views.bid_item, name="bid_item"),
    path("detail/<str:title>", views.get_listing, name="get_listing"),
    path("listings-by-cat/<str:cat>",
         views.active_by_cat,
         name="listings_by_cat"),
    path("watchlist", views.show_watchlist, name="show_watchlist"),
    path(
        "delete/<int:id>",
        views.delete_from_watchlist,
        name="delete_from_watchlist",
    ),
    path("add_to_watchlist/<str:title>",
         views.add_to_watchlist,
         name="add_to_watchlist"),
]
