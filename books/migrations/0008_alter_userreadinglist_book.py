# Generated by Django 3.2.5 on 2022-04-11 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20220411_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userreadinglist',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.books', unique=True),
        ),
    ]
