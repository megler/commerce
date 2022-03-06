# Commerce

A Django based auction application themed with Harry Potter

## Usage

In the terminal, change directory into `commerce` and run `python manage.py runserver`.

The app can now by run by pointing your browser to [localhost](http://127.0.0.1:8000/).

## Features

1. The homepage lists all active auctions. Once an auction ends, it will no longer
   show up on this page.
2. The entire card of an item listing is clickable (better UI) vs just the button.
3. The Categories link at the top of the page will list all categories.
4. On the Category Listing page (see #3) you can click on any category name and
   be taken to a page of all active listings tagged with that name.
5. If there are no active listings for a specifc category, the page will say so.
6. An individual listing page will display all relevant information, allow a
   logged in user to place a bid, add a comment and also add to their watchlist.
7. If the logged in user is also the creator of an auction, they can end that
   auction from the listing page.
8. If a logged in user is on the listing page of an auction now ended, they will
   be notified they are the highest bidder. Otherwise they will have an alert the
   auction has ended.
9. If item is already in user's watchlist, an alert will says "Item currently in
   watchlist" and give user the option to click a link to see their watchlist.
10. Watchlist can also be accessed in the top nav if user is logged in.
11. In the watchlist, a user can delete anything from the list.

# TODO's

1. Reorganize template messages where a message in 1 place (eg. "You made a bid")
   will not repeat itself when a comment is added. (eg. "Your comment was saved.")
2. Add email authentication for new user registration. (MailJet API)
3. Add stripe and a shopping cart.
4. Remove starting bid from the listings model. All bid info should be in the bid
   model only.
5. Show gravatars in comments even if user isn't currently logged in (eg. all
   comments have correct gravatars.)
