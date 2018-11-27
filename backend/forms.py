from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit,Field,Div,HTML

class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", min_length=8, max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegisterFormGuest(forms.Form):
    gender_choice = (
        ('U', 'Unknown'),
        ('M', 'Male'),
        ('F', 'Female')
    )

    years_to_display = range(datetime.now().year - 100,datetime.now().year)
    attrs={'class': 'form-control'}

    username = forms.CharField(label="Username", max_length=100,widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(label="Password", min_length=8, max_length=50,widget=forms.PasswordInput(attrs=attrs))
    firstName= forms.CharField(label="First Name", max_length=100,widget=forms.TextInput(attrs=attrs))
    lastName= forms.CharField(label="Last Name", max_length=100,widget=forms.TextInput(attrs=attrs))
    email=forms.EmailField(label="Email", max_length=100,widget=forms.TextInput(attrs=attrs))
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(),required=True)
    birthday=forms.DateField(label="Birthday",widget=forms.SelectDateWidget(years=years_to_display))
    phone=forms.RegexField(regex=r'^\+?1?\d{9,15}$')

class GuestInfoUpdateForm(forms.Form):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')
    )

    years_to_display = range(datetime.now().year - 100,datetime.now().year)
    attrs={'class': 'form-control'}

    # password = forms.CharField(label="Password", min_length=8, max_length=50,widget=forms.PasswordInput(attrs=attrs))
    firstName= forms.CharField(label="First Name", max_length=100,widget=forms.TextInput(attrs=attrs))
    lastName= forms.CharField(label="Last Name", max_length=100,widget=forms.TextInput(attrs=attrs))
    email=forms.EmailField(label="Email", max_length=100,widget=forms.TextInput(attrs=attrs))
    gender=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(),required=True)
    birthday=forms.DateField(label="Birthday",widget=forms.SelectDateWidget(years=years_to_display))
    phone=forms.RegexField(regex=r'^\+?1?\d{9,15}$')

    def __init__(self, *args, **kwargs):
        super(GuestInfoUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-description-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'updateGuestInfo'
        self.helper.add_input(Submit('Update', 'Update', css_class='btn-info'))
        self.helper.form_class = 'form-horizontal'



class RegisterFormHost(forms.Form):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')
    )
    years_to_display = range(datetime.now().year - 100,datetime.now().year)
    attrs={'class': 'form-control'}

    username = forms.CharField(label="Username", max_length=100,widget=forms.TextInput(attrs=attrs))
    firstName = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    lastName = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(label="Password", min_length=8, max_length=50,widget=forms.PasswordInput(attrs=attrs))
    email=forms.EmailField(label="Email", max_length=100,widget=forms.TextInput(attrs=attrs))
    phone=forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    birthday=forms.DateField(label="Birthday",widget=forms.SelectDateWidget(years=years_to_display))
    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(), required=True)
    location=forms.CharField(label="Location",max_length=100,widget=forms.TextInput(attrs=attrs))

class HostInfoUpdateForm(forms.Form):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown')
    )
    years_to_display = range(datetime.now().year - 100, datetime.now().year)
    attrs = {'class': 'form-control','style': 'width:30%' }

    firstName = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    lastName = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs=attrs))
    # password = forms.CharField(label="Password", min_length=8, max_length=50, widget=forms.PasswordInput(attrs=attrs))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.TextInput(attrs=attrs))
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    birthday = forms.DateField(label="Birthday", widget=forms.SelectDateWidget(years=years_to_display))
    gender = forms.ChoiceField(label="Gender", choices=gender_choice, widget=forms.Select(), required=True)
    location = forms.CharField(label="Location", max_length=100, widget=forms.TextInput(attrs=attrs))
    about = forms.CharField(label="personal description", widget=forms.Textarea(attrs={'style': 'width:70%'}))
    def __init__(self, *args, **kwargs):
        super(HostInfoUpdateForm,self).__init__( *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-description-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'updateHostInfo'
        self.helper.add_input(Submit('Update', 'Update', css_class='btn-info'))
        self.helper.form_class = 'form-horizontal'


class ListingForm(forms.Form):
    lodge_choice = (
        ('A','Apartment'),
        ('H','House'),
        ('S','Secondary unit'),
        ('U','Unique space'),
    )
    room_option=(
        ('E','Entire place'),
        ('P','Private room'),
        ('S','Shared room'),
    )
    property_type=forms.ChoiceField(label="First, let’s narrow things down",choices=lodge_choice,widget=forms.Select(attrs={'style': 'width:30%'}),required=True)
    room_type=forms.ChoiceField(label="What will guests have?",choices=room_option,widget=forms.Select(attrs={'style': 'width:30%'}),required=True)
    numberOfGuest=forms.IntegerField(label="How many guests can your place accommodate?",widget=forms.NumberInput(attrs={'style': 'width:30%'}),required=True,initial=1)
    numberOfBedroom=forms.IntegerField(label="How many bedrooms can guests use?",widget=forms.NumberInput(attrs={'style': 'width:30%'}),required=True,initial=1)
    numberOfBed = forms.IntegerField(label="How many beds can guests use?", widget=forms.NumberInput(attrs={'style': 'width:30%'}), required=True,initial=1)
    numberOfBathroom=forms.FloatField(label="How many bathrooms can guests use?",widget=forms.NumberInput(attrs={'style': 'width:30%'}),required=True,initial=1)

    def __init__(self, *args, **kwargs):
        super(ListingForm,self).__init__( *args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-Listing-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'listingEntry'
        self.helper.add_input(Submit('Next', 'Next', css_class='btn-info'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Specify the type of your lodging',
                     Field('property_type',css_class="form-control"),
                     Field('room_type', title="What will guests have",css_class="form-control"),
                     ),
            HTML("<br><br>"),
            Fieldset('Guest accommodation',
                     Field('numberOfGuest',css_class="form-control"),
                     Field('numberOfBedroom', css_class="form-control"),
                     Field('numberOfBed',css_class="form-control"),
                     Field('numberOfBathroom',css_class="form-control")
                    )
        )

class descriptionForm(forms.Form):
    name=forms.CharField(label="Name your place", max_length=100,widget=forms.TextInput(attrs={'style': 'width:70%'}))
    summary=forms.CharField(label="Summary",widget=forms.Textarea(attrs={'style': 'width:70%'}))
    cancellation_policy=forms.CharField(label="Cancellation policy (optional)",widget=forms.Textarea(attrs={'style': 'width:70%'}),required=False)
    about=forms.CharField(label="About your place (optional)",widget=forms.Textarea(attrs={'style': 'width:70%'}),required=False)
    # space=forms.CharField(label="How to get around (optional)",widget=forms.Textarea())
    note=forms.CharField(label="Other things to note (optional)",widget=forms.Textarea(attrs={'style': 'width:70%'}),required=False)
    neighbourhood_overview=forms.CharField(label="About the neighbourhood (optional)",widget=forms.Textarea(attrs={'style': 'width:70%'}),required=False)
    transit=forms.CharField(label="How to get around (optional)",widget=forms.Textarea(attrs={'style': 'width:70%'}),required=False)

    def __init__(self,*args, **kwargs):
        super(descriptionForm,self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_id = 'id-description-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'listingDescriptor'
        self.helper.add_input(Submit('Next', 'Next', css_class='btn-info'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout=Layout(
            Fieldset('Name your place',Field('name',css_class="form-control"),),
            HTML("<br><br>"),
            Fieldset('Edit your description',
                     Field('summary',css_class="form-control",rows="5"),
                     Field('cancellation_policy', css_class="form-control", rows="5"),
                     Field('about',css_class="form-control",rows="5"),
                     Field('note',css_class="form-control"),rows="5"),
            HTML("<br><br>"),
            Fieldset('The neighbourhood',
                     Field('neighbourhood_overview',css_class="form-control",rows="5"),
                     Field('transit',css_class="form-control",rows="5"),),
        )

class amenitiesForm(forms.Form):
    pet=forms.BooleanField(label="Pets in the house",required=False)
    parking = forms.BooleanField(label="Parking",required=False)
    lift = forms.BooleanField(label="Lift",required=False)
    gym = forms.BooleanField(label="Gym", required=False)
    wifi = forms.BooleanField(label="Wifi",required=False)
    fireplace = forms.BooleanField(label="Fireplace",required=False)
    hot_tub = forms.BooleanField(label="Hot tub",required=False)
    pool = forms.BooleanField(label="Pool",required=False)
    kitchen = forms.BooleanField(label="Kitchen",required=False)
    breakfast = forms.BooleanField(label="Breakfast,coffee,tea", required=False)
    air_conditioning = forms.BooleanField(label="Air conditioning", required=False)
    desk = forms.BooleanField(label="Desk/workspace", required=False)
    hairdryer= forms.BooleanField(label="Hair dryer", required=False)
    laundry_dryer = forms.BooleanField(label="Laundry – dryer", required=False)
    closet = forms.BooleanField(label="Closet/drawers", required=False)
    shampoo = forms.BooleanField(label="Shampoo", required=False)
    laundry_washer = forms.BooleanField(label="Laundry – washer", required=False)
    essentials = forms.BooleanField(label="Essentials",required=False)
    heat = forms.BooleanField(label="Heat",required=False)

    smoke_detector=forms.BooleanField(label="Smoke detector",required=False)
    carbon_monoxide_detector=forms.BooleanField(label="Carbon monoxide detector",required=False)
    first_aid_kit=forms.BooleanField(label="First aid kit",required=False)
    safety_card=forms.BooleanField(label="Safety card",required=False)
    fire_extinguisher=forms.BooleanField(label="Fire extinguisher",required=False)
    lock_on_bedroom_door=forms.BooleanField(label="Lock on bedroom door",required=False)

    def __init__(self,*args, **kwargs):
        super(amenitiesForm,self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_id = 'id-description-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'amenitiesListor'
        self.helper.add_input(Submit('Next', 'Next', css_class='btn-info'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout=Layout(
            Fieldset('What amenities do you offer?',
                     Div('pet',css_class="checkbox"),
                     Div('parking',css_class="checkbox"),
                     Div('lift', css_class="checkbox"),
                     Div('gym', css_class="checkbox"),
                     Div('wifi', css_class="checkbox"),
                     Div('fireplace', css_class="checkbox"),
                     Div('hot_tub', css_class="checkbox"),
                     Div('pool', css_class="checkbox"),
                     Div('breakfast', css_class="checkbox"),
                     Div('air_conditioning', css_class="checkbox"),
                     Div('desk', css_class="checkbox"),
                     Div('hairdryer', css_class="checkbox"),
                     Div('laundry_dryer',css_class="checkbox"),
                     Div('closet', css_class="checkbox"),
                     Div('shampoo', css_class="checkbox"),
                     Div('laundry_washer', css_class="checkbox"),
                     Div('essentials', css_class="checkbox"),
                     Div('heat', css_class="checkbox"),
                     ),
            HTML("<br><br><br>"),
            Fieldset('Safety amenities',
                     Div('smoke_detector',css_class="checkbox"),
                     Div('carbon_monoxide_detector',css_class="checkbox"),
                     Div('first_aid_kit',css_class="checkbox"),
                     Div('safety_card', css_class="checkbox"),
                     Div('fire_extinguisher', css_class="checkbox"),
                     Div('lock_on_bedroom_door', css_class="checkbox"),
            ),
        )


class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True,"class":"form-control",'style': 'width:30%'}))
    def __init__(self,*args, **kwargs):
        super(FileFieldForm,self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_id = 'id-description-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'listingScenesSetor'
        self.helper.add_input(Submit('Upload', 'Upload', css_class='btn-info'))

class SingleFileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={"class":"form-control",'style': 'width:30%'}))
    def __init__(self,*args, **kwargs):
        super(SingleFileFieldForm,self).__init__(*args, **kwargs)
        self.helper=FormHelper()
        self.helper.form_id = 'id-description-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'profilePicture'
        self.helper.add_input(Submit('Upload my profile', 'Upload my profile', css_class='btn-info'))




