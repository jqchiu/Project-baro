from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()

    def __str__(self):
        return self.name




class Photo(models.Model):
    is_main = models.BooleanField(default=False)
    url = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for listing_id: {self.listing_id} @{self.url}'




SATISFACTION = (
    ('Y', 'Would Rent Again'),
    ('N', 'Would Not Recommend Renting')
)

class Review(models.Model):
    name = models.CharField(max_length=50, default="Anonymous")
    description = models.TextField(max_length=500)
    satisfaction = models.CharField(
        max_length=15,
        choices=SATISFACTION,
        default=SATISFACTION[0][0]
    )
    published_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


INTEREST = (
    ('R', 'Rent Items'),
    ('L', 'List Items'),
    ('B', 'Rent & List Items')
)

class Profile(models.Model):
    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    interest = models.CharField(
        max_length=20,
        choices=INTEREST,
        default=INTEREST[0][0]
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    listing = models.ManyToManyField(Listing, blank=True)
    review = models.ManyToManyField(Review, blank=True)

    def __str__(self):
        return f'{self.user} profile id: {self.user.id}'
    

