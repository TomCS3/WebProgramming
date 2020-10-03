from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    pass
 
class Listing(models.Model):

    categories = [
        ('FASHION', 'Fashion'),
        ('ELECTRONICS', 'Electronics'),
        ('SPORTS', 'Sports'),
        ('HOBBIES', 'Hobbies'),
        ('HOME', 'Home'),
        ('MOTORS', 'Motors'),
        ('ART', 'Art'),
        ('BUSINESS', 'Business'),
        ('HEALTH', 'Health'),
        ('BEAUTY', 'Beauty'),
        ('MEDIA', 'Media'),
        ('OTHER', 'Other')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    category = models.CharField(choices=categories, max_length=12)
    image = models.URLField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    active = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True)
    purchaser = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("listing_detail",kwargs={"id": self.id})

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} bid ${self.price}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=150)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: "{self.comment}"'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}: is watching "{self.listing}"'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'listing'], name='unique_watching')
        ]