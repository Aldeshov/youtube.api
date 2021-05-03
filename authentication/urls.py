from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from authentication.views import UserViewSet, CurrentUser, CurrentUserProfile, ProfileAPIView, UserGenericViewSet

urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', UserViewSet.as_view({'post': 'create'})),
    path('users/me', CurrentUser.as_view()),
    path('users/me/profile', CurrentUserProfile.as_view()),
    path('users/<int:user_id>', UserGenericViewSet.as_view({'get': 'retrieve'})),
    path('users/<int:user_id>/profile', ProfileAPIView.as_view())
]
