# Generated by Django 3.2.5 on 2022-04-24 02:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_books_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreadinglist',
            name='date_read',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
