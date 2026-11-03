"""
Django Forms and Backend Validation for Tourly.
Demonstrates server-side validation alongside JavaScript frontend validation.
"""
import re
from datetime import date
from django import forms
from .models import User, Destination, TourPackage, Booking, ContactMessage


class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(max_length=150, required=True)
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, required=True)

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email address is already registered.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not re.match(r'^[+0-9\-\s]{10,15}$', phone):
            raise forms.ValidationError("Enter a valid 10 to 15 digit phone number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        cpwd = cleaned_data.get('confirm_password')
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'travel_date',
            'travelers',
            'special_requirements',
        ]

    def clean_travel_date(self):
        t_date = self.cleaned_data['travel_date']
        if t_date < date.today():
            raise forms.ValidationError("Travel date cannot be in the past.")
        return t_date

    def clean_travelers(self):
        count = self.cleaned_data['travelers']
        if count < 1 or count > 30:
            raise forms.ValidationError("Number of travelers must be between 1 and 30.")
        return count


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

    def clean_message(self):
        msg = self.cleaned_data['message'].strip()
        if len(msg) < 10:
            raise forms.ValidationError("Please provide a message of at least 10 characters.")
        return msg


class DestinationAdminForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'country', 'category', 'description', 'image', 'attractions']


class TourPackageAdminForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = [
            'destination', 'package_name', 'description', 'duration',
            'price', 'image', 'hotel_info', 'activities', 'itinerary', 'availability'
        ]
