# Generated by Django 4.2.5 on 2023-10-09 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_drivermodel_drivername_alter_verification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drivermodel',
            name='drivername',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='driver_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='verification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to=settings.AUTH_USER_MODEL),
        ),
    ]