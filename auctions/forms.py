from django.forms import ModelForm
from .models import ListAuction


class ListAuctionForm(ModelForm):
    """ Form to submit new listing """
    class Meta:
        model = ListAuction
        fields = [
            "item_name",
            "starting_bid",
            "quantity",
            "description",
            "item_condition",
            "categories",
            "listing_image",
        ]

    # Credit: https://stackoverflow.com/questions/16205908/django-modelform-not-required-field
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user")
        super(ListAuctionForm, self).__init__(*args, **kwargs)
        self.fields["listing_image"].required = False
