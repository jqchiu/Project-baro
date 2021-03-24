from django import forms
from .models import Listing, Review, Profile

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'location', 'description', 'price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'description', 'satisfaction']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'interest']