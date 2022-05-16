from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, password, **other_fields):
        """
         Creates and saves a User with the given email and other fields
        """

        if not email:
            raise ValueError('You must provide email address')
        if not phone_number:
            raise ValueError('You must provide phone number')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **other_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, first_name, last_name, password, **other_fields):
        """
        Creates and saves a superuser with the given email, and other fields
        """

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, phone_number, first_name, last_name, password, **other_fields
                                )
