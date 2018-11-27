"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from backend import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('',views.index,name='index'),
    path('admin/', admin.site.urls),
    path('loginAsGuest/', views.loginAsGuest, name='loginAsGuest'),
    path('loginAsHost/', views.loginAsHost, name='loginAsHost'),
    path('registerAsGuest/', views.registerAsGuest, name='registerAsGuest'),
    path('registerAsHost/', views.registerAsHost, name='registerAsHost'),
    path('logout/',views.logout,name="logout"),
    path('hostListingManager/',views.hostListingManager,name='hostListingManager'),
    path('listing_entry/',views.addListing,name='listingEntry'),
    path('listing_location/',views.lodgingLocation,name='lodgingLocator'),
    path('listing_description',views.setDescription,name='listingDescriptor'),
    path('listing_secenes',views.setTheScene,name='listingScenesSetor'),
    path('listing_amenities',views.setAmenities,name='amenitiesListor'),
    path('updateHostInfo',views.updateHostInfo,name="updateHostInfo"),
    path('updateGuestInfo',views.updateGuestInfo,name="updateGuestInfo"),
    path('profilePicture',views.profilePicture,name="profilePicture"),
    path('listingFinalize',views.listingFinalize,name="listingFinalize"),
    path('search/',views.search,name="search"),
    path('propertyList/',views.propertyList,name="propertyList"),
    path('checkLocation/',views.checkLocation, name="checkLocation"),
    url(r'singleProperty/(?P<listing_id>\d+)$', views.singleProperty, name='singleProperty'),
    path('addToWishlist/',views.addToWishList,name='addToWishList'),
    path('wishList/',views.getWishList, name='getWishList'),
    path('bookinghistory/',views.bookinghistory,name='bookinghistory'),
    url(r'nonmembooking/(\d+)/$',views.nonmembooking,name='nonmembooking'),
    url(r'booking/(\d+)/$', views.booking, name='booking'),
    path('deleteInWishList/',views.deleteInWishList, name='deleteInWishList'),
    path('writeReview/',views.writeReview, name='writeReview'),
    path('submitReview/',views.submitReview, name='submitReview'),
]
