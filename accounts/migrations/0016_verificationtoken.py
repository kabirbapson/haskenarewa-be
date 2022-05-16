# Generated by Django 3.2.5 on 2022-04-15 05:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20220414_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=65)),
                ('email_phone', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=6, unique=True)),
                ('expiry', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
