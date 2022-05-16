# Django

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# Third Party


# My App
from .storage import OverwriteStorage
from django.conf import settings
from .managers import MyUserManager
from books.models import Books


def save_to(instance, filename):
    # file type
    file_type = filename.split(".")[-1]

    return f"images/users/profile/{instance.id}.{file_type}"


class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="email address", unique=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=False
    )  # Validators should be a list

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=128)
    about_me = models.CharField(
        max_length=300,
        default="Hi, nice to meet you, hope you enjoy reading on Hasken Arewa",
    )
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=300)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    my_books = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    profile_picture = models.ImageField(
        upload_to=save_to, default="images/users/profile/default/profile.jpg"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    author = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_author(self):
        return self.author


class VerificationToken(models.Model):
    token = models.CharField(max_length=65)
    email_phone = models.CharField(max_length=200)
    code = models.CharField(max_length=6, unique=True)
    expiry = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email_phone


class Follow(models.Model):
    user_follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_followers",
        on_delete=models.CASCADE,
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_following",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
