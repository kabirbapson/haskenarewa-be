# Generated by Django 3.2.5 on 2022-03-29 02:28

import accounts.models
import accounts.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_myuser_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='profile_picture',
            field=models.ImageField(default='images/users/profile/default/profile.jpg', storage=accounts.storage.OverwriteStorage, upload_to=accounts.models.save_to),
        ),
    ]