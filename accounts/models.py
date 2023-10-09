from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    confirm_password = models.CharField(max_length=25)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

class DriverModel(models.Model):

    class RideType(models.Choices):
        
        pass
    drivername = models.OneToOneField(UserModel,  on_delete=models.CASCADE, related_name='driver_profile')
    location = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    passenger = models.IntegerField()
    rideType = models.CharField(max_length=20, default= 'bike')

    def __str__(self):
        return self.drivername.username
    
class Verification(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='verification')
    legal_name = models.CharField(max_length=50)
    citizenship_photo = models.ImageField(upload_to='documents/')
    phone_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.legal_name