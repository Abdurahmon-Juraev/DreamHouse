
from django.urls import path
from apps.views import PropertyListCreateView

urlpatterns = [
    path('properties/', PropertyListCreateView.as_view(), name='property-list'),
    # path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    # path('properties/<int:pk>/images/', PropertyImageUploadView.as_view(), name='property-images'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('cities/', CityListView.as_view(), name='city-list'),
    # path('districts/', DistrictListView.as_view(), name='district-list'),
    # path('send-sms-code/', SendCodeAPIView.as_view(), name='send-sms-code'),
    # path('verify-sms-code/',VerifyCodeAPIView.as_view(), name='verify-sms-code'),
]

