from django.urls import path
from .views import UserAPIView, ProductAPIView, RatingAPIView

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('products/', ProductAPIView.as_view(), name='product-list'),
    path('ratings/', RatingAPIView.as_view(), name='ratings-list'),
]
