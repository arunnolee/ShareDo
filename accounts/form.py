from django.forms import ModelForm
from .models import DriverModel, Verification

class DriverForm(ModelForm):
    class Meta:
        model = DriverModel
        fields = ['location', 'destination', 'date', 'time', 'seats', 'rideType']

class VerificationForm(ModelForm):
    class Meta:
        model = Verification
        fields = ['legal_name', 'citizenship_photo','phone_number']