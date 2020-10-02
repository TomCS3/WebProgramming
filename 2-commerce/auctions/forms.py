from django.forms import ModelForm, Form
from django.core.exceptions import ValidationError
from .models import User, Listing, Bid, Comment


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'image', 'price']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

    def __init__(self,*args,**kwargs):
        self.listing = kwargs.pop('listing', None)
        super(BidForm, self).__init__(*args,**kwargs)
    
    def clean_price(self, *args, **kwargs):
        bid_price = self.cleaned_data.get('price')
        all_bids = Bid.objects.filter(listing=self.listing)
        if all_bids:
            highest_bid = all_bids.order_by("price").last().price
            if bid_price <= highest_bid:
                raise ValidationError("Bid must be higher than the current bid")
        else:
            if bid_price < self.listing.price:
                raise ValidationError("Bid must be at least the starting asking price")
        
        return bid_price

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']