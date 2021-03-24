from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import ListingForm, ReviewForm, ProfileForm 
from .models import Listing, Photo, Review, Profile
from django.db.models import Q

import uuid
import boto3

S3_BASE_URL = 'https://s3-us-west-2.amazonaws.com/'
BUCKET = 'project-baro'

def home(request):
    return render(request, 'home.html')



def about(request):
    return render(request, 'about.html')



def listings_index(request):
    listings = Listing.objects.all()
    return render(request, 'listings/index.html', { 'listings' : listings, 'current_user': request.user })



def listings_detail(request, listing_id):
    listings = Listing.objects.get(id=listing_id)
    review_form = ReviewForm()
    return render(request, 'listings/detail.html', { 
        'listing': listings, 
        'review_form': review_form,
        'current_user': request.user 
    })



def list_an_item(request):
    if request.method == 'POST':
        listing_form = ListingForm(request.POST)

        if listing_form.is_valid():
            listing_form.save()
            return redirect('index')

    else:
        listing_form = ListingForm()
        return render(request, 'listings/add.html', { 'listing_form': listing_form })



def edit_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'GET':
        listing_form = ListingForm(instance=listing)
        return render(request, 'listings/edit.html', { 'form': listing_form })

    else:
        listing_form = ListingForm(request.POST, instance=listing)
        if listing_form.is_valid():
            listing_form.save()
            return redirect('detail', listing_id=listing_id)



def delete_listing(request, listing_id):
    if request.method == 'POST':
        Listing.objects.get(id=listing_id).delete()
        return redirect('index')



def add_review(request, listing_id):
    review_form = ReviewForm(request.POST)

    if review_form.is_valid():
        new_review = review_form.save(commit=False)
        new_review.listing_id = listing_id
        new_review.save()
    
    return redirect('detail', listing_id=listing_id)



def edit_review(request, listing_id, review_id):
    listing = Listing.objects.get(id=listing_id)
    review = Review.objects.get(id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('detail', listing_id=listing_id)
    else:
        form = ReviewForm(instance=review)
        context = {
            'form': form,
            'listing': listing,
            'review': review
        }
    return render(request, 'review-post/edit.html', context)



def delete_review(request, listing_id, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('detail', listing_id=listing_id)



def add_photo(request, listing_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, listing_id=listing_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
    return redirect('detail', listing_id=listing_id)



# def delete_photo(request, listing_id, photo_id):
#     photo = Photo.objects.get(id=photo_id)
#     if request.method == 'POST':
#         photo.delete()
#         return redirect('detail', listing_id=listing_id)



def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_profile')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)



def profile(request):
    context = {
        'current_user': request.user
    }
    return render(request, 'users/profile.html', context)



def create_profile(request):
    error_message = ''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('profile')
    form = ProfileForm()
    context = {'form': form}
    return render(request, 'users/create_profile.html', context)



def search(request):
    query=None
    results = []
    if request.method == 'GET':
        query = request.GET.get('search')
        results = Listing.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(price__icontains=query)
        )
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'search.html', context)