from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, filters
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Property, City, District, PropertyImage
from .serializers import PropertySerializer, CitySerializer, DistrictSerializer, PropertyImageSerializer

class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.select_related('city','district','agent').prefetch_related('images').all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'city__name', 'district__name']
    ordering_fields = ['price', 'created_at']

    def perform_create(self, serializer):

        if hasattr(self.request.user, 'agent_profile'):
            serializer.save(agent=self.request.user.agent_profile)
        else:
            serializer.save()
