# Generated by Django 3.2.5 on 2022-04-06 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_myuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='author',
            field=models.BooleanField(default=False),
        ),
    ]