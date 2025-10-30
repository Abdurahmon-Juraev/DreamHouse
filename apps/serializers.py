from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import City, District, Agent, Property, PropertyImage

User = get_user_model()

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'city']

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'phone', 'company']

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
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all(), source='agent', write_only=True, required=False)

    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'agent', 'agent_id', 'property_type',
            'transaction_type', 'price', 'currency', 'city', 'district', 'address',
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
