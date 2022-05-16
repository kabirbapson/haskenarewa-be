# Django
from posixpath import basename
from django.urls import path


# rest framework
from rest_framework.routers import DefaultRouter
# Knox
from knox import views as knox_views


# My App
from .api import ConfirmVerificationAPI, FollowAPI, GetAuthorAPI, PasswordResetAPI, PasswordResetChangeAPI, PasswordResetRequestAPI, UpdateUserProfileAPI, UserAPI, LoginAPI, RegisterAPI, VerificationAPI

router = DefaultRouter()
router.register(r'author', GetAuthorAPI, basename='author')

urlpatterns = [
    path('user', UserAPI.as_view(), name='user'),
    path('update', UpdateUserProfileAPI),
    path('register', RegisterAPI.as_view(), name='register'),
    path('verify', VerificationAPI, name='email-phone-verification'),
    path('verify-confirmation', ConfirmVerificationAPI,
         name='confirm verification'),
    path('reset-password-request', PasswordResetRequestAPI,
         name='reset-password-request'),
    path('reset-password-verify', PasswordResetAPI,
         name='reset-password-verify'),
    path('reset-password-change', PasswordResetChangeAPI,
         name='reset-password-change'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('follow', FollowAPI),
    path('follow/<int:pk>/', FollowAPI),


    #     path('author/<int:pk>/', GetAuthorAPI),


]

urlpatterns += router.urls
