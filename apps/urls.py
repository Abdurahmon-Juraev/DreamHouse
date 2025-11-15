from apps.views import LoginAPIView, PropertyDetailAPIView, PropertyListCreateView, SendCodeAPIView
from django.urls import path

urlpatterns = [
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    path('properties/<int:pk>/', PropertyDetailAPIView.as_view(), name='property-detail'),
    # path('properties/<int:pk>/images/', PropertyImageUploadView.as_view(), name='property-images'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('cities/', CityListView.as_view(), name='city-list'),
    # path('districts/', DistrictListView.as_view(), name='district-list'),
    # path('send-sms-code/', SendCodeAPIView.as_view(), name='send-sms-code'),
    # path('verify-sms-code/',VerifyCodeAPIView.as_view(), name='verify-sms-code'),
]
