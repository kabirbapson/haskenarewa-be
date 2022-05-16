# Generated by Django 3.2.5 on 2022-04-19 18:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_alter_userreadinglist_user'),
        ('accounts', '0017_myuser_about_me'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLibrary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('books', models.ManyToManyField(to='books.Books')),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
