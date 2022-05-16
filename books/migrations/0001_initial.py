# Generated by Django 3.2.5 on 2022-04-06 23:43

import books.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=255, null=True)),
                ('book_cover', models.ImageField(default='images/books/cover/default/default.png', upload_to=books.models.save_to)),
                ('publication_date', models.DateField(blank=True, null=True)),
                ('language', models.CharField(default='English', max_length=255)),
                ('book_summary', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.BigIntegerField(default=0)),
                ('readers', models.BigIntegerField(default=0)),
                ('ratings', models.FloatField(default=0.0)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='books.books')),
            ],
        ),
    ]
