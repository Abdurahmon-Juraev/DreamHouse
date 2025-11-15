from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Property
from .serializers import PropertySerializer, SendSmsCodeSerializer, VerifySmsCodeSerializer
from .utils import check_sms_code, random_code, send_sms_code


@extend_schema(tags=['Auth'])
class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = request.data.get('phone')
        code = random_code()
        valid, _ttl = send_sms_code(phone, code)
        if valid:
            return Response({"message": "send sms code"})

        return Response({"detail": f"You can send again in {int(_ttl)} seconds"})


@extend_schema(tags=['Auth'])
class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)


class PropertyListCreateView(ListCreateAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def perform_create(self, serializer):

        if hasattr(self.request.user, 'agent_profile'):
            serializer.save(agent=self.request.user.agent_profile)
        else:
            serializer.save()


class PropertyDetailAPIView(RetrieveAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
