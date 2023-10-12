from django.forms import ModelForm
from .models import DriverModel, Verification, ClientModel

class DriverForm(ModelForm):
    class Meta:
        model = DriverModel
        fields = ['location', 'destination', 'date', 'time', 'seats', 'rideType']

class ClientForm(ModelForm):
    class Meta:
        model = ClientModel
        fields =['location', 'destination', 'date', 'time', 'seats','passenger', 'rent']

class VerificationForm(ModelForm):
    class Meta:
        model = Verification
        fields = ['legal_name', 'citizenship_photo','phone_number']