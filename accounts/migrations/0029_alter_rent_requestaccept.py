# Generated by Django 4.2.5 on 2023-12-10 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_alter_rent_requestaccept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='requestAccept',
            field=models.BooleanField(default=None),
        ),
    ]