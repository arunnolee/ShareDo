from django.contrib import admin
from accounts.models import UserModel
from accounts import models

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserModel, UserAdmin)
# admin.site.register(models.DriverModel)
admin.site.register(models.Verification)
# admin.site.register(models.ClientModel)
admin.site.register(models.RideModel)
