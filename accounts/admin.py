from django.contrib import admin
from accounts.models import UserModel
from django.utils.html import format_html
from accounts import models

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserModel, UserAdmin)
admin.site.register(models.Verification)
admin.site.register(models.RideModel)
admin.site.register(models.ContactUsModel)
admin.site.register(models.Rent)

class DriverVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_photo', 'display_license', 'is_verified', )

    def display_photo(self, obj):
        return format_html('<img src="{}" width="70%" />', obj.photo.url)

    display_photo.short_description = 'Photo'

    def display_license(self, obj):
        return format_html('<img src="{}" width="70%" />', obj.license.url)

    display_license.short_description = 'License'

admin.site.register(models.DriverVerification, DriverVerificationAdmin)