# Generated by Django 4.2.5 on 2023-11-30 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_ridemodel_accept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridemodel',
            name='clientname',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]