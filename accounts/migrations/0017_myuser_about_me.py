# Generated by Django 3.2.5 on 2022-04-17 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_verificationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='about_me',
            field=models.CharField(default='Hi, Nice to Meet you!, Happy reading on Hasken Arewa', max_length=300),
        ),
    ]
