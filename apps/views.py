from random import randint

from drf_spectacular.utils import extend_schema
from rest_framework import permissions, generics, filters
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Property
from .serializers import PropertySerializer, SendSmsCodeSerializer, VerifySmsCodeSerializer
from .utils import send_code


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.select_related('city', 'district', 'agent').prefetch_related('images').all()
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


from rest_framework.views import APIView
from rest_framework.response import Response


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data['phone']
        code = randint(100_000, 999_999)
        send_code(phone, code)
        return Response({"message": "send sms code"})


@extend_schema(tags=['Auth'])
class VerifyCodeAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_data())
