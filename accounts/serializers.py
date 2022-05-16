# Django

from accounts.models import Follow
from books.serializers import BookSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

# Django rest framework
from rest_framework import serializers

from payment import models


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id", "email", "first_name", "last_name", "phone_number", 'date_of_birth',
            'profile_picture', 'gender', 'country', 'state', 'address', 'is_verified', 'about_me', 'likes',
        )


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',
                  'first_name', 'last_name', 'email', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User.objects.create_user(

            email=validated_data['email'], phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'], last_name=validated_data['last_name'],
            password=validated_data['password'],

        )

        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError(
            "Incorrect Password or Email Address")


class VerificationSerializer(serializers.Serializer):
    verification_type = serializers.CharField()
    email_phone = serializers.CharField()


class ConfirmVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email_phone = serializers.CharField()


class ConfirmVerificationPassSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email_phone = serializers.CharField()
    new_password = serializers.CharField()


class AuthorProfileSerializer(serializers.Serializer):
    book = BookSerializer(read_only=True)

    id = serializers.IntegerField()
    profile_picture = serializers.ImageField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    about_me = serializers.CharField()
    my_books = serializers.IntegerField()
    likes = serializers.IntegerField()
    is_verified = serializers.BooleanField()


class FollowProfileSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    # profile_picture = serializers.ImageField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserFollowSerializer(serializers.ModelSerializer):
    user_follower = FollowProfileSerializer()
    following = FollowProfileSerializer()

    class Meta:
        model = Follow
        fields = "__all__"


class UpdateUserProfileSerializer(serializers.Serializer):
    about_me = serializers.CharField()
