import re
from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .models import City, District, Property, PropertyImage, User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SendSmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')

        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs):
        phone = attrs['phone']
        user, created = User.objects.get_or_create(phone=phone)
        user.set_unusable_password()

        return super().validate(attrs)


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField(default=100100)
    token_class = RefreshToken

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        return phone.removeprefix('998')

    def validate(self, attrs: dict[str, Any]):
        phone_number = attrs['phone']

        try:
            user_obj = User.objects.get(phone=phone_number)

            authenticated_user = authenticate(phone=phone_number, request=self.context['request'])
            if authenticated_user is not None:
                self.user = authenticated_user
            else:
                if not user_obj.is_active:
                    raise ValidationError("Foydalanuvchi faol emas. Ma'muriyatga murojaat qiling.")
                self.user = user_obj

        except User.DoesNotExist:
            try:
                self.user = User.objects.create(phone=phone_number)
            except Exception as e:
                print(f"User yaratishda xato: {e}")
                raise ValidationError(
                    "Foydalanuvchini yaratishda kutilmagan xato yuz berdi. Iltimos, keyinroq urinib ko'ring.")

        if self.user is None or not self.user.is_active:
            raise ValidationError("Foydalanuvchini topish, yaratish yoki faollikni tekshirishda xato yuz berdi.")

        return attrs

    @property
    def get_data(self):
        refresh = self.get_token(self.user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }
        user_data = UserModelSerializer(self.user).data

        return {
            'message': "OK",
            'data': {
                **data, **{'user': user_data}
            }
        }

    @classmethod
    def get_token(cls, user) -> Token:
        return cls.token_class.for_user(user)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'city']


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']
        read_only_fields = ['id']


class PropertySerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    images_upload = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'agent', 'agent_id', 'property_type',
            'transaction_type', 'price', 'currency', 'region', 'district', 'address',
            'rooms', 'residential_complex',
            'created_at', 'updated_at', 'images', 'images_upload',
        ]
        read_only_fields = ['created_at', 'updated_at', 'images', 'agent']

    def create(self, validated_data):
        images_data = validated_data.pop('images_upload', [])
        property_obj = super().create(validated_data)

        for img in images_data:
            PropertyImage.objects.create(property=property_obj, image=img)
        return property_obj

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images_upload', [])
        property_obj = super().update(instance, validated_data)
        for img in images_data:
            PropertyImage.objects.create(property=property_obj, image=img)
        return property_obj
