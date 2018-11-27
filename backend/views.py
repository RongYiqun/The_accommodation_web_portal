from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms,models
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from imghdr import what
import os
from project.settings import STATIC_PATH
import hashlib
import geocoder
from django.http import JsonResponse
import datetime
import time
from django.core.mail import send_mail
from random import randrange




googleKey="AIzaSyB1Gtog4Cv8OUO6FuheLR_94UkhekmPZuI"


def md5(f):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def index(request):
    popular_listing = models.Listing.objects.filter(review_scores_rating__isnull=False).order_by('-review_scores_rating','-number_of_reviews')[:9]
    most_popular = {'id':popular_listing[0].id,'name': popular_listing[0].name, 'picture':popular_listing[0].picture_url}
    results = []
    for item in popular_listing[1:]:
        results.append({'id':item.id,'name': item.name, 'picture':item.picture_url})
    if request.user.id:
        recommends = recommendation(request.user.id)
        return render(request, 'search.html',{'base_template_name': 'base.html', 'message': '', 'most_popular': most_popular, 'results': results,'recommendation':recommends})

    return render(request,'search.html',{'base_template_name': 'base.html','message':'','most_popular':most_popular,'results':results})


def loginAsGuest(request):
    message = ""
    login_form = forms.UserForm(request.POST)
    if request.method == 'POST':
        user=None
        message = "Please check the details!"
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
        if user and models.Visitor.objects.filter(username=username).exists():
            auth.login(request, user)
            request.session['role']="guest"
            return HttpResponseRedirect('/index/')
        else:
            message="User does not exist or Incorrect password!"
            return render(request, 'loginAsGuest.html',locals())
    else:
        return render(request, 'loginAsGuest.html', locals())


def loginAsHost(request):
    message = ""
    login_form = forms.UserForm(request.POST)
    if request.method == 'POST':
        user = None
        message = "Please check the details!"
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
        if user and models.Host.objects.filter(username=username).exists():
            auth.login(request, user)
            request.session['role']="host"
            return HttpResponseRedirect('/index/')
        else:
            message = "User does not exist or Incorrect password!"
            return render(request, 'loginAsHost.html', locals())
    else:
        return render(request, 'loginAsHost.html', locals())

def registerAsGuest(request):
    # RegisterForm = forms.RegisterFormGuest()
    message = ""
    if request.method == 'POST':
        form = forms.RegisterFormGuest(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email=form.cleaned_data['email']
            gender=form.cleaned_data['gender']
            phone=form.cleaned_data['phone']
            firstName=form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            newUser=models.Visitor()
            if not models.Visitor.objects.filter(username=username).exists() \
                    or not models.Visitor.objects.filter(email=email):
                newUser = models.Visitor()
                newUser.email = email
                newUser.username = username
                newUser.set_password(password)
                newUser.phone=phone
                newUser.gender=gender
                newUser.first_name=firstName
                newUser.last_name=lastName
                newUser.save()
                message="you have registered"
                return redirect('/index/')
            else:
                message="username or email already exist"
        else:
            message="invalid input"
    else:
        RegisterForm = forms.RegisterFormGuest()
    return render(request, 'registerAsGuest.html', locals())

def updateGuestInfo(request):  #update
    dict={}
    if request.method == 'POST':
        form = forms.GuestInfoUpdateForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']

            gender = form.cleaned_data['gender']
            birthday = form.cleaned_data['birthday']

            HostObject = models.Visitor.objects.get(myuser_ptr_id=request.user.id)
            usrObject=models.Myuser.objects.get(id=request.user.id)
            HostObject.gender=gender
            HostObject.birthday=birthday
            HostObject.save()

            usrObject.phone=phone
            usrObject.email=email
            # usrObject.set_password(password)
            usrObject.first_name=firstName
            usrObject.last_name=lastName
            usrObject.save()
            return redirect('/index/')

    HostObject = models.Visitor.objects.get(myuser_ptr_id=request.user.id)
    usrObject = models.Myuser.objects.get(id=request.user.id)

    if usrObject.password is not None:
        dict['password']=usrObject.password
    if usrObject.email is not None:
        dict['email']=usrObject.email
    if usrObject.phone is not None:
        dict['phone']=usrObject.phone
    if usrObject.first_name is not None:
        dict['firstName']=usrObject.first_name
    if usrObject.last_name is not None:
        dict['lastName']=usrObject.last_name

    if HostObject.birthday is not None:
        dict['birthday']=HostObject.birthday
    if HostObject.gender is not None:
        dict['gender']=HostObject.gender

    GuestInfoUpdateForm = forms.GuestInfoUpdateForm(initial=dict)
    return render(request, 'guestInfoUpdate.html', locals())


def registerAsHost(request):  #here2
    RegisterForm = forms.RegisterFormHost()
    message = ""
    if request.method == 'POST':
        form = forms.RegisterFormHost(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            location=form.cleaned_data['location']
            birthday=form.cleaned_data['birthday']
            gender=form.cleaned_data['gender']

            newUser = models.Host()
            if not models.Host.objects.filter(username=username).exists() \
                    or not models.Host.objects.filter(email=email):
                newUser = models.Host()
                newUser.email = email
                newUser.username = username
                newUser.set_password(password)
                newUser.phone = phone
                newUser.first_name = firstName
                newUser.last_name = lastName
                newUser.location=location
                newUser.since=datetime.datetime.now()
                newUser.birthday=birthday
                newUser.gender=gender
                newUser.save()
                message = "you have registered"
                return redirect('/index/')
            else:
                message = "username or email already exist"
        else:
            message = "invalid input"
    else:
        RegisterForm = forms.RegisterFormHost()
    return render(request, 'registerAsHost.html', locals())


def updateHostInfo(request):  #update
    dict={}
    if request.method == 'POST':
        form = forms.HostInfoUpdateForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']

            location = form.cleaned_data['location']
            gender = form.cleaned_data['gender']
            about = form.cleaned_data['about']
            birthday = form.cleaned_data['birthday']

            HostObject = models.Host.objects.get(myuser_ptr_id=request.user.id)
            usrObject=models.Myuser.objects.get(id=request.user.id)
            HostObject.about=about
            HostObject.location=location
            HostObject.gender=gender
            HostObject.birthday=birthday
            HostObject.save()

            usrObject.phone=phone
            usrObject.email=email
            # usrObject.set_password(password)
            usrObject.first_name=firstName
            usrObject.last_name=lastName
            usrObject.save()
            return redirect('/index/')

    HostObject = models.Host.objects.get(myuser_ptr_id=request.user.id)
    usrObject = models.Myuser.objects.get(id=request.user.id)

    if usrObject.email is not None:
        dict['email']=usrObject.email
    if usrObject.phone is not None:
        dict['phone']=usrObject.phone
    if usrObject.first_name is not None:
        dict['firstName']=usrObject.first_name
    if usrObject.last_name is not None:
        dict['lastName']=usrObject.last_name

    if HostObject.birthday is not None:
        dict['birthday']=HostObject.birthday
    if HostObject.gender is not None:
        dict['gender']=HostObject.gender
    if HostObject.location is not None:
        dict['location']=HostObject.location
    if HostObject.about is not None:
        dict['about']=HostObject.about

    photo="/pictures/e1b5f44d998ccbf08cf5571d45e93cbb.png"
    if HostObject.picture is not None:
        photo=HostObject.picture

    HostInfoUpdateForm = forms.HostInfoUpdateForm(initial=dict)
    SingleFileFieldForm=forms.SingleFileFieldForm()
    return render(request, 'hostInfoUpdate.html', locals())

def profilePicture(request):
    if request.method == 'POST':
        picture_fomate = set(['jpeg', 'png', 'gif'])
        f = request.FILES.getlist('file_field')[0]
        formate = what(f)
        if formate in picture_fomate:
            HostObject = models.Host.objects.get(myuser_ptr_id=request.user.id)
            name = str(md5(f))
            currentName = name + '.' + formate
            full_filename = os.path.join(STATIC_PATH, "pictures", currentName)
            with open(full_filename, 'w+b') as fl:
                f.seek(0)
                bytes = bytearray(f.read())
                fl.write(bytes)
            HostObject.picture = "pictures/" + currentName
            HostObject.save()
    return  HttpResponseRedirect(reverse('updateHostInfo'))
    # return redirect('/index/')


def logout(request):
    auth.logout(request)
    return render(request,"logout.html")

def hostListingManager(request):  #alllist
    if 'listing_id' in request.session:
        del request.session['listing_id']

    if request.method=='GET':
        if request.user is not None and request.user.is_authenticated:
            listings=[]
            result=models.Listing.objects.filter(host_id=request.user.id)
            if result.exists():
                for ele in result:
                    listings.append((ele.name,ele.city,ele.id))
            return render(request, 'HostRegister/AllListings.html', locals())
    elif request.method=='POST':
        listingID=int(request.POST.get('listingID'))
        ifRemove=int(request.POST.get('ifRemove'))
        if ifRemove==0:
            if listingID==-1:
                return HttpResponseRedirect(reverse('listingEntry'))
            else:
                request.session['listing_id'] = listingID
                return HttpResponseRedirect(reverse('listingEntry'))
        else:
            if models.Listing.objects.filter(pk=listingID,host_id=request.user.id).exists():
                if models.Images.objects.filter(listing_id=listingID).exists():
                    for ele in models.Images.objects.filter(listing_id=listingID):
                        ele.delete()
                currentObject = models.Listing.objects.get(pk=listingID)
                currentObject.delete()
                listings = []
                if models.Listing.objects.filter(host_id=request.user.id).exists():
                    for ele in models.Listing.objects.filter(host_id=request.user.id):
                        listings.append((ele.name, ele.city, ele.id))
            return render(request, 'HostRegister/AllListings.html', locals())


def addListing(request):
    listingForm = None
    if request.method == 'POST':
        form = forms.ListingForm(request.POST)
        if form.is_valid():
            property_type = form.cleaned_data['property_type']
            room_type = form.cleaned_data['room_type']
            numberOfGuest = form.cleaned_data['numberOfGuest']
            numberOfBedroom = form.cleaned_data['numberOfBedroom']
            numberOfBed = form.cleaned_data['numberOfBed']
            numberOfBathroom = form.cleaned_data['numberOfBathroom']
            currentObject=None
            if 'listing_id' in request.session:
                currentListingID=request.session['listing_id']
                currentObject = models.Listing.objects.get(pk=currentListingID)
            else:
                currentObject = models.Listing()
            currentObject.property_type = property_type
            currentObject.room_type = room_type
            currentObject.accommodates = numberOfGuest
            currentObject.bed = numberOfBed
            currentObject.bedrooms = numberOfBedroom
            currentObject.bathrooms = numberOfBathroom
            currentObject.host_id = request.user.id
            currentObject.save()
            request.session['listing_id'] = currentObject.id
            return HttpResponseRedirect(reverse('amenitiesListor'))
    else:

        if 'listing_id' in request.session:
            currentListingID = request.session['listing_id']
            currentObject = models.Listing.objects.get(pk=currentListingID)
            listingForm = forms.ListingForm(initial={
                "property_type":currentObject.property_type,
                "room_type":currentObject.room_type,
                "numberOfGuest":currentObject.accommodates,
                "numberOfBedroom":currentObject.bedrooms,
                "numberOfBed":currentObject.bed,
                "numberOfBathroom":currentObject.bathrooms
                })
        else:
            listingForm = forms.ListingForm()
    return render(request, 'HostRegister/listYourPlace.html', locals())

def lodgingLocation(request):
    if request.method=="POST":
        if 'listing_id' in request.session:
            Listing_id = int(request.session['listing_id'])
            currentObject = models.Listing.objects.get(pk=Listing_id)
            latitude = request.POST.get('latitude', 0)
            longitude = request.POST.get('longitude', 0)
            currentObject.latitude=latitude
            currentObject.longitude=longitude
            g=geocoder.google([str(latitude),str(longitude)],method='reverse',key=googleKey)
            if g.ok:
                currentObject.city=g.city
                currentObject.save()
                return HttpResponseRedirect(reverse('listingDescriptor'))
            else:
                defautlatitude = -33.9163798
                defautlongitude = 151.2325216
                return render(request, "HostRegister/location.html", locals())
        else:
            defautlatitude = -33.9163798
            defautlongitude = 151.2325216
            return render(request, "HostRegister/location.html", locals())

    else:
        defautlatitude=-33.9163798
        defautlongitude=151.2325216
        if 'listing_id' in request.session:
            Listing_id = int(request.session['listing_id'])
            currentObject = models.Listing.objects.get(pk=Listing_id)
            if currentObject.latitude is not None and currentObject.longitude is not None:
                defautlatitude=currentObject.latitude
                defautlongitude=currentObject.longitude
        return render(request,"HostRegister/location.html",locals())


def setTheScene(request):  #here1
    FileFieldForm = forms.FileFieldForm()
    template_name = 'HostRegister/setTheScene.html'
    if request.method == 'POST':
        ifRemove=request.POST.get('ifRemove')
        if ifRemove is not None:
            imgID = int(request.POST.get('imgID'))
            check=models.Images.objects.filter(id=imgID)
            if check.exists():
                for ele in check:
                    ele.delete()
            return HttpResponseRedirect(reverse('listingScenesSetor'))
        else:
            picture_fomate = set(['jpeg', 'png', 'gif'])
            files = request.FILES.getlist('file_field')
            for f in files:
                formate=what(f)
                if formate in picture_fomate:
                    Listing_id = int(request.session['listing_id'])
                    Pictures=models.Images()
                    Pictures.listing_id=Listing_id
                    name=str(md5(f))
                    currentName=name+'.'+formate
                    full_filename = os.path.join(STATIC_PATH, "pictures", currentName)
                    with open(full_filename, 'w+b') as fl:
                        f.seek(0)
                        bytes = bytearray(f.read())
                        fl.write(bytes)
                    Pictures.picture_url="pictures/"+currentName
                    Pictures.save()
            return HttpResponseRedirect(reverse('listingScenesSetor'))
            # return render(request,"HostRegister/finished.html")
    else:
        Listing_id = int(request.session['listing_id'])
        photoList=[]
        checkedResult=models.Images.objects.filter(listing_id=Listing_id)
        if checkedResult.exists():
            for ele in checkedResult:
                photoList.append((ele.id,ele.picture_url))
        return render(request,template_name,locals())

#Am
def setAmenities(request):
    amenitiesForm = None
    if request.method == 'POST':
        form = forms.amenitiesForm(request.POST)
        if form.is_valid():
            amenitiesList=['pet','parking','lift','gym','wifi','fireplace','hot_tub','pool','kitchen','breakfast',
                           'air_conditioning','desk','hairdryer','laundry_dryer','closet','shampoo','laundry_washer',
                           'essentials','heat','smoke_detector','carbon_monoxide_detector','first_aid_kit','safety_card',
                           'fire_extinguisher','lock_on_bedroom_door']
            if 'listing_id' in request.session:
                Listing_id = int(request.session['listing_id'])
                currentObject = models.Listing.objects.get(pk=Listing_id)
                amenities_info=[]
                for i in range(len(amenitiesList)):
                    flag=form.cleaned_data[amenitiesList[i]]
                    if flag:
                        amenities_info.append(amenitiesList[i])
                amenitiesString = '{'
                for x in amenities_info:
                    amenitiesString += x
                    amenitiesString += ','
                amenitiesString = amenitiesString[:-1]
                amenitiesString += '}'
                currentObject.amenities=amenitiesString
                currentObject.save()
                return HttpResponseRedirect(reverse('lodgingLocator'))
            else:
                listingForm = forms.amenitiesForm()
                return render(request, 'HostRegister/amenities.html', locals())
    else:
        if 'listing_id' in request.session:
            currentListingID = request.session['listing_id']
            currentObject = models.Listing.objects.get(pk=currentListingID)
            newDict={}
            if currentObject.amenities is not None:
                for amenity in currentObject.amenities.split(','):
                    newDict[amenity]=True
                amenitiesForm = forms.amenitiesForm(initial=newDict)
            else:
                amenitiesForm = forms.amenitiesForm()
        else:
            amenitiesForm = forms.amenitiesForm()
    return render(request, 'HostRegister/amenities.html', locals())

def setDescription(request):
    descriptionForm = None
    if request.method == 'POST':
        form = forms.descriptionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            summary = form.cleaned_data['summary']
            about = form.cleaned_data['about']
            note = form.cleaned_data['note']
            neighbourhood_overview = form.cleaned_data['neighbourhood_overview']
            transit = form.cleaned_data['transit']
            cancellation_policy = form.cleaned_data['cancellation_policy']
            Listing_id=int(request.session['listing_id'])
            currentObject=models.Listing.objects.get(pk=Listing_id)
            currentObject.name = name
            currentObject.summary = summary
            currentObject.about = about
            currentObject.note = note
            currentObject.cancellation_policy= cancellation_policy
            currentObject.neighbourhood_overview=neighbourhood_overview
            currentObject.transit=transit
            currentObject.save()
            return HttpResponseRedirect(reverse('listingScenesSetor'))
    else:
        if 'listing_id' in request.session:
            currentListingID = request.session['listing_id']
            currentObject = models.Listing.objects.get(pk=currentListingID)
            newDict={"name":currentObject.name,
                "summary":currentObject.summary}
            if hasattr(currentObject,"about"):
                newDict["about"]=currentObject.about
            if hasattr(currentObject,"note"):
                newDict["note"]=currentObject.note
            if hasattr(currentObject,"neighbourhood_overview"):
                newDict["neighbourhood_overview"]=currentObject.neighbourhood_overview
            if hasattr(currentObject,"transit"):
                newDict["transit"]=currentObject.transit
            descriptionForm=forms.descriptionForm(initial=newDict)
        else:
            descriptionForm = forms.descriptionForm()
    return render(request, 'HostRegister/addDescription.html', locals())


def listingFinalize(request):
    currentListingID = request.session['listing_id']
    currentObject = models.Listing.objects.get(pk=currentListingID)
    currentObject.price=randrange(200,500)
    currentObject.host_id=request.user.id
    currentObject.cleaning_fee=randrange(0,20)
    currentObject.minimum_nights=1
    currentObject.review_scores_rating=90
    currentObject.number_of_reviews=0
    HostObject = models.Host.objects.get(myuser_ptr_id=request.user.id)
    if HostObject.picture!=None:
        currentObject.host_picture_url='/static/'+HostObject.picture
    else:
        currentObject.host_picture_url = '/static/user.png'
    currentObject.host_about=HostObject.about
    Userobject = models.Myuser.objects.get(id=request.user.id)
    currentObject.host_name=Userobject.first_name
    check=models.Images.objects.filter(listing_id=currentListingID)
    if check.exists():
        currentObject.picture_url='/static/'+check[0].picture_url
    currentObject.save()
    return HttpResponseRedirect('/index/')


def search(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/index/')

    results = []
    num_of_guests = 0
    location = ''
    c_in = ''
    c_out = ''
    guests = ''

    if request.method == 'POST':
        location = request.POST.get('where')
        c_in = request.POST.get('check-in')
        c_out = request.POST.get('check-out')
        guests = request.POST.get('guests')
        request.session['c_in'] = c_in
        request.session['c_out'] = c_out
        request.session['guests'] = guests

        if guests == "1 guest":
            num_of_guests = 1
        elif guests == "2 guests":
            num_of_guests = 2
        elif guests == "3 guests":
            num_of_guests = 3
        elif guests == "4 guests":
            num_of_guests = 4
        elif guests == "5+ guests":
            num_of_guests = 5
        find_results = models.Listing.objects.filter(city__icontains=location).filter(accommodates__gte=num_of_guests)


        popular_listing = models.Listing.objects.filter(review_scores_rating__isnull=False).order_by('-review_scores_rating','-number_of_reviews')[:9]
        most_popular = {'id':popular_listing[0].id,'name': popular_listing[0].name, 'picture':popular_listing[0].picture_url}
        rr2 = []
        for item in popular_listing[1:]:
            rr2.append({'id':item.id,'name': item.name, 'picture':item.picture_url})

        if request.user.id:
            recommands = recommendation(request.user.id)
            if location == '':
                return render(request, 'search.html',
                              {"err_message": "Please enter the location!", 'most_popular': most_popular,
                               'results': rr2, 'recommendation':recommands})
            elif c_in == '':
                return render(request, 'search.html',
                              {"err_message": "Please enter check-in date!", 'most_popular': most_popular,
                               'results': rr2, 'recommendation':recommands})
            elif c_out == '':
                return render(request, 'search.html',
                              {"err_message": "Please enter check-out date!", 'most_popular': most_popular,
                               'results': rr2, 'recommendation':recommands})
            elif guests == '':
                return render(request, 'search.html',
                              {"err_message": "Please enter number of guests!", 'most_popular': most_popular,
                               'results': rr2, 'recommendation':recommands})

        if location == '':
            return render(request,'search.html',{"err_message":"Please enter the location!",'most_popular':most_popular,'results':rr2})
        elif c_in == '':
            return render(request,'search.html',{"err_message":"Please enter check-in date!",'most_popular':most_popular,'results':rr2})
        elif c_out == '':
            return render(request,'search.html',{"err_message":"Please enter check-out date!",'most_popular':most_popular,'results':rr2})
        elif guests == '':
            return render(request,'search.html',{"err_message":"Please enter number of guests!",'most_popular':most_popular,'results':rr2})

        for each in find_results:
            results.append({"id":each.id,"url":each.picture_url,"name":each.name,"price":each.price})

        return render(request,'propertyList.html',{'results': results, 'number':len(results)})

def propertyList(request):
    return render(request,'propertyList.html',{'base_template_name': 'base_afterlogin.html'})

def singleProperty(request, listing_id):
    listing = models.Listing.objects.filter(id= listing_id)
    reviews = models.Reviews.objects.filter(listing_id=listing_id).order_by('-reviews_date')
    comments = []
    for x in reviews:
        comments.append({'review_name':x.reviewer_name, 'review_data':x.reviews_date, 'comments':x.comments})
    if len(comments) >= 10:
        comments = comments[:10]
    item = listing[0]
    L = []
    for y in item.amenities[1:-1].split(","):
        L.append(y.replace('"',''))
    results = {'name':item.name, 'summary':item.summary, 'space':item.space, 'transit':item.transit,'picture':item.picture_url,
                'host_name':item.host_name, 'host_picture':item.host_picture_url, 'host_about':item.host_about, 'accommodates': item.accommodates,
                'bedroom':item.bedrooms, 'bathroom':item.bathrooms, 'amenities':L, 'price':item.price, 'latitude':item.latitude, 'longitude':item.longitude,
                'clean_fee':item.cleaning_fee, 'rating':item.review_scores_rating}
    return render(request,'singleProperty.html',{'listing_id': listing_id, 'result':results, 'comments':comments})


def checkLocation(request):
    location=request.POST.get('location','')
    locator=geocoder.google(location.strip(),key=googleKey)
    newDict={}
    if locator.ok:
        newDict["status"]=True
        newDict["latitude"]= locator.latlng[0]
        newDict["longitude"]=locator.latlng[1]
    else:
        newDict["status"]=False
        newDict["latitude"] = -1
        newDict["longitude"] = -1
    return JsonResponse(newDict)

def addToWishList(request):
    userid = request.user.id
    listingid = request.POST.get('listingid')
    if not models.Wish_list.objects.filter(user_id=userid, wish_listings=listingid).exists():
        newWishList = models.Wish_list()
        newWishList.user_id = userid
        newWishList.wish_listings = listingid
        newWishList.save()
    return render(request, 'singleProperty.html')

def getWishList(request):
    userid = request.user.id
    wishList = models.Wish_list.objects.filter(user_id=userid)
    results = []
    for x in wishList:
        listingid = x.wish_listings
        listing = models.Listing.objects.filter(id=listingid)
        item = listing[0]
        amenities_num = len(item.amenities.split(","))
        if item.review_scores_rating == None:
            rate = 0.0
        else:
            rate = item.review_scores_rating / 20
        if amenities_num < 10:
            temp = 'fewer accommodates'
        elif amenities_num > 20:
            temp = 'abundant accommodates'
        else:
            temp = 'moderate accommodates'
        singleInfo = {'id': item.id, 'name': item.name, 'picture':item.picture_url, 'price':item.price,
                      'clean_fee': item.cleaning_fee, 'rating': rate,
                      'room_type':item.room_type.replace('/apt',''), 'number_of_reviews': item.number_of_reviews,
                      'accommodates': item.accommodates, 'bedroom':item.bedrooms, 'bathroom':item.bathrooms, 'number_of_amenities':temp}
        results.append(singleInfo)
    return render(request, 'wishList.html', {'results' : results})

def deleteInWishList(request):
    userid = request.user.id
    listingid = request.POST.get('listingid')
    wishListing = models.Wish_list.objects.filter(user_id=userid, wish_listings=listingid)
    wishListing.delete()

    return render(request, 'wishList.html')


def booking(request,listing_id):
    if 'c_in' in request.session:
        pre_cin = request.session['c_in']
    else:
        pre_cin = ''
    if 'c_out' in request.session:
        pre_cout = request.session['c_out']
    else:
        pre_cout = ''
    if 'guests' in request.session and request.session['guests']!="":
        pre_guests = int(request.session['guests'].split()[0])
    else:
        pre_guests = ''
    non_flag = 0
    if request.method == 'GET':
        each = models.Listing.objects.filter(id = listing_id)
        if pre_cin=='' or pre_cout=='' or pre_guests=='':
            dd = 0
            total_price = 0
            pre_cin = ''
            pre_cout = ''
            pre_guests = 1
            non_flag = 1
        else:
            d1 = datetime.datetime(int(pre_cin.split('-')[2]),int(pre_cin.split('-')[1]),int(pre_cin.split('-')[0]))
            d2 = datetime.datetime(int(pre_cout.split('-')[2]),int(pre_cout.split('-')[1]),int(pre_cout.split('-')[0]))
            dd = (d2 - d1).days
            if dd<1:
                dd = 1
            each = models.Listing.objects.filter(id = listing_id)
            if each[0].cleaning_fee!=None:
                total_price = float(each[0].price)*dd + float(each[0].cleaning_fee)
            else:
                total_price = float(each[0].price)*dd
        return render(request,'booking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
        'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
        'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag,'err':0})
    else:
        c_in = request.POST.get('check-in')
        c_out = request.POST.get('check-out')
        each = models.Listing.objects.filter(id = listing_id)
        if pre_cin=='' or pre_cout=='' or pre_guests=='':
            dd = 0
            total_price = 0
            pre_cin = ''
            pre_cout = ''
            pre_guests = 1
            non_flag = 1
        total_price = 0

        newbooking = models.Bookings()
        newbooking.listing_id = listing_id
        newbooking.visitor_id = request.user.id
        newbooking.start_date = c_in.split('-')[2]+"-"+ c_in.split('-')[1]+"-"+c_in.split('-')[0]
        newbooking.end_date = c_out.split('-')[2]+"-"+ c_out.split('-')[1]+"-"+c_out.split('-')[0]
        d1 = datetime.datetime(int(c_in.split('-')[2]),int(c_in.split('-')[1]),int(c_in.split('-')[0]))
        d2 = datetime.datetime(int(c_out.split('-')[2]),int(c_out.split('-')[1]),int(c_out.split('-')[0]))
        dd = (d2 - d1).days
        if dd<1:
            dd = 1
        if each[0].cleaning_fee!=None:
            newbooking.total_price = float(each[0].price)*dd + float(each[0].cleaning_fee)
        else:
            newbooking.total_price = float(each[0].price)*dd

        check_start = c_in.split('-')[2]+"-"+ c_in.split('-')[1]+"-"+c_in.split('-')[0]
        check_end = c_out.split('-')[2]+"-"+ c_out.split('-')[1]+"-"+c_out.split('-')[0]
        if check_validation(listing_id,check_start,check_end)==False:
            return render(request,'booking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
            'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
            'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag,'err':1})

        newbooking.save()
        return render(request,'finishbooking.html',{'listing_id':listing_id})


def bookinghistory(request):
    if request.method == 'POST':
        del_id = int(request.POST.get('bookingID'))
        ifRemove = int(request.POST.get('ifRemove_'+str(del_id)))
        if ifRemove==1:
            models.Bookings.objects.filter(booking_id = del_id).delete()
    curr_id = request.user.id
    each = models.Bookings.objects.filter(visitor_id = curr_id)
    results = []
    for x in each:
        e_listing = models.Listing.objects.filter(id = x.listing_id)
        results.append({'booking_id':x.booking_id,'listing_id':e_listing[0].id,'name':e_listing[0].name, 'picture':e_listing[0].picture_url,
        'start_date':x.start_date, 'end_date':x.end_date, 'total_price':x.total_price})
    return render(request, 'bookinghistory.html',{'results': results})



def nonmembooking(request,listing_id):
    if 'c_in' in request.session:
        pre_cin = request.session['c_in']
    else:
        pre_cin = ''
    if 'c_out' in request.session:
        pre_cout = request.session['c_out']
    else:
        pre_cout = ''
    if 'guests' in request.session and request.session['guests']!="":
        pre_guests = int(request.session['guests'].split()[0])
    else:
        pre_guests = ''
    non_flag = 0
    if request.method == 'GET':
        each = models.Listing.objects.filter(id = listing_id)
        if pre_cin=='' or pre_cout=='' or pre_guests=='':
            dd = 0
            total_price = 0
            pre_cin = ''
            pre_cout = ''
            pre_guests = 1
            non_flag = 1
        else:
            d1 = datetime.datetime(int(pre_cin.split('-')[2]),int(pre_cin.split('-')[1]),int(pre_cin.split('-')[0]))
            d2 = datetime.datetime(int(pre_cout.split('-')[2]),int(pre_cout.split('-')[1]),int(pre_cout.split('-')[0]))
            dd = (d2 - d1).days
            if dd<1:
                dd = 1
            each = models.Listing.objects.filter(id = listing_id)
            if each[0].cleaning_fee!=None:
                total_price = float(each[0].price)*dd + float(each[0].cleaning_fee)
            else:
                total_price = float(each[0].price)*dd
        return render(request,'nonmembooking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
        'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
        'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag})

    else:
        c_in = request.POST.get('check-in')
        c_out = request.POST.get('check-out')
        v_name = request.POST.get('v_name')
        v_phone = request.POST.get('v_phone')
        v_email = request.POST.get('v_email')
        each = models.Listing.objects.filter(id = listing_id)
        if pre_cin=='' or pre_cout=='' or pre_guests=='':
            dd = 0
            total_price = 0
            pre_cin = ''
            pre_cout = ''
            pre_guests = 1
            non_flag = 1
        total_price = 0

        d1 = datetime.datetime(int(c_in.split('-')[2]),int(c_in.split('-')[1]),int(c_in.split('-')[0]))
        d2 = datetime.datetime(int(c_out.split('-')[2]),int(c_out.split('-')[1]),int(c_out.split('-')[0]))
        dd = (d2 - d1).days


        newbooking = models.Nonmembookings()
        newbooking.listing_id = listing_id
        newbooking.visitor_name = v_name
        newbooking.visitor_phone = v_phone
        newbooking.visitor_email = v_email
        newbooking.start_date = c_in.split('-')[2]+"-"+ c_in.split('-')[1]+"-"+c_in.split('-')[0]
        newbooking.end_date = c_out.split('-')[2]+"-"+ c_out.split('-')[1]+"-"+c_out.split('-')[0]

        if dd<1:
            dd = 1
        if each[0].cleaning_fee!=None:
            newbooking.total_price = float(each[0].price)*dd + float(each[0].cleaning_fee)
            total_price = float(each[0].price)*dd + float(each[0].cleaning_fee)
        else:
            newbooking.total_price = float(each[0].price)*dd
            total_price = float(each[0].price)*dd

        if v_name == "":
            return render(request,'nonmembooking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
            'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
            'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag,'err':"Please enter your name!"})
        if v_phone == "":
            return render(request,'nonmembooking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
            'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
            'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag,'err':"Please enter your phone!"})
        if v_email == "":
            return render(request,'nonmembooking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
            'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
            'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag,'err':"Please enter your email!"})

        check_start = c_in.split('-')[2]+"-"+ c_in.split('-')[1]+"-"+c_in.split('-')[0]
        check_end = c_out.split('-')[2]+"-"+ c_out.split('-')[1]+"-"+c_out.split('-')[0]
        if check_validation(listing_id,check_start,check_end)==False:
            return render(request,'nonmembooking.html',{'listing_id':listing_id,'picture':each[0].picture_url,'name':each[0].name,
            'price':each[0].price,'clean_fee':each[0].cleaning_fee,'pre_cin':pre_cin,'pre_cout':pre_cout,'pre_guests':pre_guests,
            'pre_dd':dd,'pre_price':int(each[0].price)*dd,'total_price':int(total_price),'non_flag':non_flag,'err':"Please choose another time!"})

        booking_reference = "NONMEM-"+str(int(time.time()))
        newbooking.booking_reference = booking_reference
        newbooking.save()

        email_message = '''
Dear customer {}:
    You have successfully booked an accommodation.
    Your booking renference is {}.
    Here is the link: www.lehuoingpage.com/singleProperty/{}
    The check-in date is {} and the check-out date is {}.
    Please note the total fee is ${}.
Thanks!
'''.format(v_name,booking_reference,listing_id,c_in,c_out,total_price)

        send_mail('Booking succeed', email_message, 'z5129023@ad.unsw.edu.au',
        [v_email], fail_silently=False)
        return HttpResponseRedirect('/index/')



def check_validation(id,c_in,c_out):

    t_dset = dateRange(c_in,c_out)
    af = models.Bookings.objects.filter(listing_id = id)
    for each in af:
        p_dset = dateRange(str(each.start_date),str(each.end_date))
        if len(t_dset & p_dset) != 0:
            return False

    lf = models.Nonmembookings.objects.filter(listing_id = id)
    for each in lf:
        l_dset = dateRange(str(each.start_date),str(each.end_date))
        if len(t_dset & l_dset) != 0:
            return False
    return True



def dateRange(bgn, end):
    fmt = '%Y-%m-%d'
    bgn = int(time.mktime(time.strptime(bgn,fmt)))
    end = int(time.mktime(time.strptime(end,fmt)))
    d_list = [time.strftime(fmt,time.localtime(i)) for i in range(bgn,end+1,3600*24)]
    d_set = set()
    for each in d_list:
        d_set.add(each)
    return d_set


def writeReview(request):
    listing_id = request.POST.get('listing_id')

    return render(request, 'writeReview.html', {'listing_id':listing_id})

def submitReview(request):
    listing_id = request.POST.get('listing_id')
    comment = request.POST.get('review')
    user_id = request.user.id
    user_name = models.Visitor.objects.filter(id=user_id)[0].username

    if not models.Reviews.objects.filter(listing_id=listing_id, reviewer_id=user_id).exists():
        newReview = models.Reviews()
        newReview.listing_id = listing_id
        newReview.comments = comment
        newReview.reviewer_id = user_id
        newReview.reviewer_name = user_name
        newReview.reviews_date = datetime.date.today()
        newReview.save()

    return HttpResponseRedirect(reverse('singleProperty',kwargs={'listing_id':listing_id}))

def recommendation(user_id):
    previous_bookings = models.Bookings.objects.filter(visitor_id=user_id)
    if len(previous_bookings) == 0:
        return []
    listing_ids = []
    locations = []
    price = []
    for item in previous_bookings:
        listing_ids.append(item.listing_id)
        pre_booking = models.Listing.objects.filter(id=item.listing_id)
        locations.append(pre_booking[0].city)
        price.append(pre_booking[0].price)
    if len(price) == 1:
        max_price = price[0] + 100
        min_price = max(price[0] - 100, 50)
    else:
        max_price = max(price)
        min_price = min(price)
    recommend_listings = models.Listing.objects.filter(city__in=locations,review_scores_rating__isnull=False)\
        .order_by('-review_scores_rating','-number_of_reviews')
    results = []
    for x in recommend_listings:
        if x.price != None:
            if x.price >= min_price and x.price <= max_price and x.id not in listing_ids:
                results.append({'id': x.id, 'name': x.name, 'picture': x.picture_url})
    if len(results) > 4:
        results = results[:4]
    return results
