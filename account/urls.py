from django.urls import path
from .views import (
    UserOwnView,
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
    path('profile/<int:pk>/', UserOwnView.as_view(), name='profile'),
    path('profile/update/<int:pk>/', UserDetailView.as_view(), name='profile_update'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('verify-email/', EmailVerificationView.as_view()),
    path('change-password/<int:pk>/', ChangePasswordView.as_view())
]
