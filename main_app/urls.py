from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('listings/', views.listings_index, name='index'),
    path('listings/<int:listing_id>/', views.listings_detail, name='detail'),

    path('listings/add', views.list_an_item, name='list_an_item'),
    path('listings/<int:listing_id>/edit', views.edit_listing, name="edit_listing"),
    path('listings/<int:listing_id>/delete', views.delete_listing, name="delete_listing"),

    path('listings/<int:listing_id>/add-review>', views.add_review, name="add_review"),
    path('listings/<int:listing_id>/<int:review_id>/edit-review', views.edit_review, name="edit_review"),
    path('listings/<int:listing_id>/<int:review_id>/delete-review', views.delete_review, name="delete_review"),

    path('accounts/signup/', views.signup, name="signup"),
    path('users/profile/', views.profile, name='profile'),
    path('users/create-profile', views.create_profile, name="create_profile"),

    path('listings/<int:listing_id>/add_photo', views.add_photo, name="add_photo"),
    # path('listings/<int:listing_id>/<int:photo_id>/delete-photo', views.delete_photo, name="delete_photo"),
    path('search/', views.search, name='search'),
]








# u:joal pw:JoalChiu123