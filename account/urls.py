from django.urls import path
from .views import (
    RegisterView,
    LoginAPIView,
    LogoutAPIView,
    UserListView,
    UserDetailView,
    EmailVerificationView,
    ChangePasswordView
)

urlpatterns = [
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='profile_detail'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('verify-email/', EmailVerificationView.as_view()),
    path('change-password/<int:pk>/', ChangePasswordView.as_view())
]
