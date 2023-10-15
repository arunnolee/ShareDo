from django.forms import ModelForm
from .models import Verification, RideModel

# class DriverForm(ModelForm):
#     class Meta:
#         model = DriverModel
#         fields = ['location', 'destination', 'date', 'time', 'seats', 'rideType']

# class ClientForm(ModelForm):
#     class Meta:
#         model = ClientModel
#         fields =['location', 'destination', 'date', 'time', 'seats', 'rideType', 'passenger', 'rent']

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
        fields = ['passenger', 'rent']