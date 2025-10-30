from typing import Any

from django.db.models import CharField
from jsonschema.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.fields import IntegerField
from rest_framework.serializers import Serializer
import re
from apps.models import City, District, User, Property, PropertyImage
from apps.utils import check_phone
from rest_framework_simplejwt.tokens import RefreshToken


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'city']

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone']

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']
        read_only_fields = ['id']

class PropertySerializer(serializers.ModelSerializer):
    # read-only nested
    images = PropertyImageSerializer(many=True, read_only=True)
    # write-only field for uploading multiple files in create/update
    images_upload = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    agent = UserModelSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='agent', write_only=True, required=False)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'agent', 'agent_id', 'property_type',
            'transaction_type', 'price', 'currency', 'district', 'address',
            'rooms', 'area', 'is_new_building', 'residential_complex',
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

class SendSmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone.removeprefix('998')


class VerifySmsCodeSerializer(Serializer):
    phone = CharField(default='901001010')
    code = IntegerField(default=100100)
    token_class = RefreshToken

    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            **tokens, **user_data
        }
        return data

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid = check_phone(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})
        phone = attrs['phone']

        self.user, _ = User.objects.get_or_create(phone=phone)
        attrs['user'] = self.user
        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)  # type: ignore


    default_error_messages = {
        "no_active_account": "No active account found with the given credentials"
    }

    def validate_phone(self, value):
        digits = re.findall(r'\d', value)
        if len(digits) < 9:
            raise ValidationError('Phone number must be at least 9 digits')
        phone = ''.join(digits)
        if len(phone) > 9 and phone.startswith('998'):
            phone = phone.removeprefix('998')
        return phone

    def get_data(self):
        refresh = self.get_token(self.user)
        user_data = UserModelSerializer(self.user).data

        tokens = {
            'access token': str(refresh.access_token),
            'refresh token': str(refresh)
        }
        data = {
            'message': 'Valid Code',
            **tokens, **user_data
        }
        return data

    def validate(self, attrs: dict[str, Any]) -> dict[Any, Any]:
        is_valid = check_phone(**attrs)
        if not is_valid:
            raise ValidationError({'message': 'invalid or expired code'})
        phone = attrs['phone']

        self.user, _ = User.objects.get_or_create(phone=phone)
        attrs['user'] = self.user
        return attrs

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)





