# Python
from multiprocessing import context
from books.models import Books
from books.serializers import BookSerializer
from .serializers import AuthorProfileSerializer, ConfirmVerificationPassSerializer, ConfirmVerificationSerializer, UpdateUserProfileSerializer, User, UserFollowSerializer, UserSerializer, RegisterSerializer, LoginSerializer, VerificationSerializer
from accounts.models import Follow, VerificationToken
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, permissions, viewsets, status
import string
import random
import secrets

# django
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()


# RestFramework


# Knox


# My App


def generateOTP():
    digits = string.digits
    ranges = 6

    code = ''.join(random.choices(digits, k=ranges))
    return code


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        }, 201)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


@api_view(['POST'])
def VerificationAPI(request):

    serializer = VerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if len(User.objects.all().filter(email=serializer.data['email_phone'])) != 0:
        return Response({'status': 'failed', 'reason': 'User with the same email already exist'}, status=status.HTTP_400_BAD_REQUEST)

    with open(f'{settings.BASE_DIR}/accounts/templates/Verification.html') as file:
        html_template = file.read()
        otp = generateOTP()
    my_message = f"""Email Verification!

Please verify your email address

{otp}

We are reaching you because this email has been used to create an account on Hasken Arewa. Kindly use the code above to verify your email address.

It will expire in 30 minutes"""

    send_mail_status = send_mail(
        subject='Email Verification',
        message=my_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[serializer.data['email_phone']],
        fail_silently=False,
    )

    if send_mail_status == 0:
        return Response({'status': 'failed', 'reason': 'failed to send verification to this email'}, status=status.HTTP_400_BAD_REQUEST)

    token = secrets.token_hex()
    user = VerificationToken(
        token=token, email_phone=serializer.data['email_phone'], code=otp)
    user.save()
    return Response({'status': 'success', "email_phone": user.email_phone, "token": token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ConfirmVerificationAPI(request):

    session_token = request.headers.get('Session', None)
    try:
        user_token = VerificationToken.objects.get(token=session_token)
    except Exception as error:
        user_token = None

    if session_token == None or user_token == None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = ConfirmVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if serializer.data['otp'] != user_token.code:
        return Response({'status': 'failed', 'reason': 'invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)

    user_token.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def VerificationAPI(request):

    serializer = VerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if len(User.objects.all().filter(email=serializer.data['email_phone'])) != 0:
        return Response({'status': 'failed', 'reason': 'User with the same email already exist'}, status=status.HTTP_400_BAD_REQUEST)

    with open(f'{settings.BASE_DIR}/accounts/templates/Verification.html') as file:
        html_template = file.read()
        otp = generateOTP()
    my_message = f"""Email Verification!

Please verify your email address

{otp}

We are reaching you because this email has been used to create an account on Hasken Arewa. Kindly use the code above to verify your email address.

It will expire in 30 minutes"""

    send_mail_status = send_mail(
        subject='Email Verification',
        message=my_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[serializer.data['email_phone']],
        fail_silently=False,
    )

    if send_mail_status == 0:
        return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

    token = secrets.token_hex()
    user = VerificationToken(
        token=token, email_phone=serializer.data['email_phone'], code=otp)
    user.save()
    return Response({'status': 'success', "email_phone": user.email_phone, "token": token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def PasswordResetRequestAPI(request):

    serializer = VerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if len(User.objects.all().filter(email=serializer.data['email_phone'])) == 0:
        return Response({'status': 'failed', 'reason': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    with open(f'{settings.BASE_DIR}/accounts/templates/Verification.html') as file:
        html_template = file.read()
        otp = generateOTP()
    my_message = f"""Hi {serializer.data['email_phone']},

We received a request to reset your Hasken Arewa password.
Enter the following password reset code:

{otp}

Didn't request this change?
If you didn't request a new password, let us know."""

    send_mail_status = send_mail(
        subject='Password Reset',
        message=my_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[serializer.data['email_phone']],
        fail_silently=False,
    )

    if send_mail_status == 0:
        return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

    token = secrets.token_hex()
    user = VerificationToken(
        token=token, email_phone=serializer.data['email_phone'], code=otp)
    user.save()
    return Response({'status': 'success', "email_phone": user.email_phone, "token": token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def PasswordResetAPI(request):

    session_token = request.headers.get('Session', None)
    try:
        user_token = VerificationToken.objects.get(token=session_token)
    except Exception as error:
        user_token = None

    if session_token == None or user_token == None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = ConfirmVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if serializer.data['otp'] != user_token.code or serializer.data['email_phone'] != user_token.email_phone:
        return Response({'status': 'failed', 'reason': 'not a valid verification code or email'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def PasswordResetChangeAPI(request):
    session_token = request.headers.get('Session', None)

    try:
        user_token = VerificationToken.objects.get(token=session_token)
    except Exception as error:
        user_token = None

    if session_token == None or user_token == None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = ConfirmVerificationPassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if serializer.data['otp'] != user_token.code:
        return Response({'status': 'failed', 'reason': 'not a valid verification code'}, status=status.HTTP_400_BAD_REQUEST)

    user_token.delete()
    user = User.objects.get(email=user_token.email_phone)
    user.set_password(serializer.data['new_password'])
    user.save()

    user_serializer = UserSerializer(user)

    return Response({'user': user_serializer.data, 'token': AuthToken.objects.create(user)[1]}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ChangePasswordAPI(request):

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def GetAuthorAPI(request, pk=None):
    try:
        book = Books.objects.get(id=pk)
    except Exception as error:
        print(error)
        return Response(status=404)

    author = book.author
    books = Books.objects.all().filter(author=author)
    book_serializer = BookSerializer(books, many=True)
    serializer = AuthorProfileSerializer(author)


class GetAuthorAPI(viewsets.ReadOnlyModelViewSet):

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AuthorProfileSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):

        pk = self.kwargs['pk']

        try:
            book = Books.objects.get(id=pk)
        except Exception as error:
            print(error)
            return Response(status=404)

        author = book.author
        books = Books.objects.all().filter(author=author)
        book_serializer = BookSerializer(
            books, context={'request': request}, many=True)
        author_serializer = AuthorProfileSerializer(
            author, context={'request': request},)

        author_data = author_serializer.data

        followers = len(Follow.objects.filter(following=author))
        following = len(Follow.objects.filter(user_follower=author))

        author_data['followers'] = followers
        author_data['following'] = following

        return Response({'author': author_data, 'books': book_serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def FollowAPI(request, pk=None):
    if request.method == 'GET' and pk == None:
        follow = Follow.objects.filter(
            following=request.user) | Follow.objects.filter(user_follower=request.user)

        serializer = UserFollowSerializer(follow, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'GET' and pk != None:
        user_to_follow = User.objects.get(pk=pk)

        # check if user already follow
        check_if_follow = Follow.objects.filter(
            user_follower=request.user).filter(following=user_to_follow)

        if len(check_if_follow) != 0:
            check_if_follow[0].delete()
            follow = Follow.objects.filter(
                following=request.user) | Follow.objects.filter(user_follower=request.user)

            serializer = UserFollowSerializer(follow, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        Follow.objects.create(user_follower=request.user,
                              following=user_to_follow)

        follow = Follow.objects.filter(
            following=request.user) | Follow.objects.filter(user_follower=request.user)

        serializer = UserFollowSerializer(follow, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        return Response('still', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateUserProfileAPI(request, pk=None):
    serializer = UpdateUserProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user

    if request.FILES.get('profile_picture', None) != None:
        user.profile_picture = request.FILES['profile_picture']
    user.about_me = serializer.data['about_me']

    user.save()

    serializer = UserSerializer(user, context={'request': request})

    return Response(serializer.data, status=status.HTTP_201_CREATED)
