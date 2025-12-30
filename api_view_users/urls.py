from django.urls import path
from .views import UserListAPIView, UserDetailAPIView, UserDetailByUsernameAPIView, UserListAPIViewQueryParam

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/filter/', UserListAPIViewQueryParam.as_view(), name='user-filter'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/<str:username>/', UserDetailByUsernameAPIView.as_view(), name='user-detail-by-username'),
]