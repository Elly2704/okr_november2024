from django.urls import path, include
from oauth2_provider.views import TokenView

from .views import UserCreateApiView, UserUpdateDeleteApiView, UserLoginView
from django.urls import path

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('o/token/', TokenView.as_view(), name='token'),

    path('users/', UserCreateApiView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserUpdateDeleteApiView.as_view(), name='user-detail-update-delete'),

]
