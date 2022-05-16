# Generated by Django 3.2.5 on 2022-04-11 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_categories_categoryitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='genre',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='categories',
            name='books',
            field=models.ManyToManyField(to='books.Books'),
        ),
    ]