from django.db import models
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    confirm_password = models.CharField(max_length=25)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']
    
class Verification(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='verification')
    legal_name = models.CharField(max_length=50)
    citizenship_photo = models.ImageField(upload_to='documents/')
    phone_number = models.CharField(max_length=15)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class DriverVerification(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='driver_verification')
    photo = models.ImageField(upload_to="driver_doc")
    license = models.ImageField(upload_to="driver_doc")
    is_verified = models.BooleanField(default=False)

class RideModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    drivername = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="driver_profile", null=True)
    location = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    seats = models.IntegerField()
    rideType = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.location} to {self.destination}"
    
    @property
    def available_seats(self):
        return self.seats - self.passenger
    
class Rent(models.Model):
    REQUEST_ACCEPT_CHOICES = (
        ("A", "Accepted"),
        ("R", "Rejected"),
        ("P", "Pending")
    )
    created_on = models.DateTimeField(auto_now_add=True)
    user_client = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name="rent")
    ride = models.ForeignKey('RideModel', on_delete=models.CASCADE, related_name="ride")
    rent = models.CharField(max_length=5)
    requestAccept = models.CharField(max_length=1, choices=REQUEST_ACCEPT_CHOICES, default="P")

    def __str__(self):
        return self.user_client.username

class ContactUsModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    message = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
