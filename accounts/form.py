from django.forms import ModelForm
from .models import Verification, RideModel, ContactUsModel, Rent, DriverVerification

class VerificationForm(ModelForm):
    class Meta:
        model = Verification
        fields = ['legal_name', 'citizenship_photo','phone_number']

class DriverRideForm(ModelForm):
    class Meta:
        model = RideModel
        fields = ['location', 'destination', 'date', 'time', 'seats', 'rideType']

class ClientRideForm(ModelForm):
    class Meta:
        model = RideModel
        fields = ['location']

class ContactUsForm(ModelForm):
    class Meta:
        model = ContactUsModel
        fields = ['name', 'email', 'message']

class RentForm(ModelForm):
    class Meta:
        model = Rent
        fields = ['requestAccept']


class DriverVerificationForm(ModelForm):
    class Meta:
        model = DriverVerification
        fields = ["photo", "license"]