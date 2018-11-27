from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Myuser(AbstractUser):
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    verification = models.BooleanField(default=False)

class Visitor(Myuser):
    gender_choice = (
        ('M','Male'),
        ('F','Female'),
        ('U','Unknown')
    )
    gender = models.CharField(max_length=1,choices=gender_choice,default='U')
    birthday = models.DateField(blank=True,null=True)
    portrait = models.ImageField(blank=True,null=True)
    good_credit = models.BooleanField(default=True)



class Host(Myuser):
    gender_choice = (
        ('M','Male'),
        ('F','Female'),
        ('U','Unknown')
    )
    good_credit = models.BooleanField(default=True)
    gender = models.CharField(max_length=1,choices=gender_choice,default='U')
    birthday = models.DateField(blank=True,null=True)
    verifications = models.TextField(blank=True, null=True)
    picture = models.URLField(blank=True,null=True)
    since=models.DateField(blank=True,null=True)
    about=models.TextField(blank=True,null=True)
    location=models.TextField(blank=True,null=True)





class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=True,null=True)
    summary = models.TextField(blank=True,null=True)
    space = models.TextField(blank=True,null=True)
    neighbourhood_overview = models.TextField(blank=True,null=True)
    notes = models.TextField(blank=True,null=True)  #
    transit = models.TextField(blank=True,null=True)
    picture_url = models.URLField(blank=True,null=True)
    host_id = models.BigIntegerField()  #
    host_name = models.TextField(blank=True,null=True) #
    host_since = models.DateField(blank=True,null=True) #
    host_location = models.TextField(blank=True,null=True) #
    host_about = models.TextField(blank=True,null=True)  #
    host_picture_url = models.URLField(blank=True,null=True) #
    host_total_listings_count = models.IntegerField(blank=True,null=True) #
    host_verifications = models.TextField(blank=True,null=True) #
    city = models.CharField(blank=True,max_length=200,null=True)
    state = models.CharField(blank=True,max_length=200,null=True)
    zipcode = models.IntegerField(blank=True,null=True)  #
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    property_type = models.CharField(blank=True,max_length=200,null=True)
    room_type = models.CharField(blank=True,max_length=200,null=True)
    accommodates = models.IntegerField(blank=True,null=True)
    bathrooms = models.FloatField(blank=True,null=True)
    bedrooms = models.IntegerField(blank=True,null=True)
    bed = models.IntegerField(blank=True,null=True)
    bed_type = models.CharField(blank=True,max_length=200,null=True)
    amenities = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True) #
    cleaning_fee = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    minimum_nights = models.IntegerField(blank=True,null=True) #
    number_of_reviews = models.IntegerField(blank=True,null=True)
    review_scores_rating = models.IntegerField(blank=True,null=True)
    cancellation_policy = models.TextField(blank=True,null=True) #


class Calendar(models.Model):
    listing_id = models.BigIntegerField()
    calendar_date = models.DateField(blank=True,null=True)
    available = models.BooleanField()
    price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)


class Reviews(models.Model):
    listing_id = models.BigIntegerField()
    id = models.AutoField(primary_key=True)
    reviews_date = models.DateField(blank=True,null=True)
    reviewer_id = models.BigIntegerField()
    reviewer_name = models.CharField(blank=True,max_length=200,null=True)
    comments = models.TextField(blank=True,null=True)

class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    listing_id = models.BigIntegerField()
    visitor_id = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    cancellation = models.BooleanField(default=False)

class Nonmembookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    listing_id = models.BigIntegerField()
    visitor_name = models.TextField(blank=True,null=True)
    visitor_phone = models.TextField(blank=True,null=True)
    visitor_email = models.TextField(blank=True,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=True)
    booking_reference = models.TextField(blank=True,null=True)


class Images(models.Model):
    listing_id = models.BigIntegerField()
    picture_url = models.URLField(blank=True,null=True)



class Wish_list(models.Model):
    user_id = models.IntegerField()
    wish_listings = models.IntegerField(blank=True,null=True)
