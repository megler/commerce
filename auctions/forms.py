from django.forms import ModelForm, Textarea
from .models import ListAuction, Bid


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
        widgets = {
            "description": Textarea(attrs={"rows": 5}),
        }

    # Credit: https://stackoverflow.com/questions/16205908/django-modelform-not-required-field
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop("user")
        super(ListAuctionForm, self).__init__(*args, **kwargs)
        self.fields["listing_image"].required = False
        self.fields["categories"].required = False
        self.fields["item_name"].widget.attrs.update({"class": "form-control"})
        self.fields["starting_bid"].widget.attrs.update(
            {"class": "form-control"})
        self.fields["quantity"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update(
            {"class": "form-control"})
        self.fields["item_condition"].widget.attrs.update(
            {"class": "form-control"})
        self.fields["categories"].widget.attrs.update(
            {"class": "form-control"})
        self.fields["listing_image"].widget.attrs.update(
            {"class": "form-control"})
