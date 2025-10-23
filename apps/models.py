# app/property/py
from django.contrib.auth import get_user_model
from django.db.models import Model, ForeignKey, OneToOneField, CASCADE, SET_NULL, ImageField, CharField, TextField, \
    DecimalField, PositiveSmallIntegerField, \
    BooleanField, DateTimeField
from django.db.models.enums import TextChoices

User = get_user_model()

CURRENCY_CHOICES = [
    ('UZS', "so'm"),
    ('USD', 'USD'),
]

TRANSACTION_CHOICES = [
    ('sale', 'Sale'),
    ('rent', 'Rent'),
]

PROPERTY_TYPE_CHOICES = [
    ('apartment', 'Apartment'),
    ('house', 'House'),
    ('land', 'Land'),
    ('office', 'Office'),
    ('res_complex', 'Residential complex'),
]

ROOM_CHOICES = [(i, f"{i}-room") for i in range(1, 6)]


class City(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class District(Model):
    city = ForeignKey(City, related_name='districts', on_delete=CASCADE)
    name = CharField(max_length=100)

    def __str__(self):
        return f"{self.name} — {self.city.name}"


class Agent(Model):
    user = OneToOneField(User, on_delete=CASCADE, related_name='agent_profile')
    phone = CharField(max_length=30, blank=True, null=True)
    company = CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class ResidentialComplex(Model):
    name = CharField(max_length=255)
    city = ForeignKey(City, on_delete=SET_NULL, null=True, blank=True)
    address = CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Property(Model):
    class Currency(TextChoices):
        USD = 'usd', 'Dollar'
        UZS = 'uzs', "So'm"

    title = CharField(max_length=255)  # +
    description = TextField(blank=True)  # ckeditor5
    agent = ForeignKey(Agent, related_name='properties', on_delete=SET_NULL, null=True, blank=True)
    property_type = CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    transaction_type = CharField(max_length=10, choices=TRANSACTION_CHOICES, default='sale')
    price = DecimalField(max_digits=15, decimal_places=2)  # +
    currency = CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)  # +
    region = ForeignKey('apps.City', CASCADE)  # +
    district = ForeignKey('apps.District', CASCADE)  # +
    address = CharField(max_length=255, blank=True, null=True)  # +
    # location = ?
    rooms = PositiveSmallIntegerField(choices=ROOM_CHOICES, null=True, blank=True)
    area = DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # sqm
    is_new_building = BooleanField(default=False)
    residential_complex = ForeignKey(ResidentialComplex, on_delete=SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.city.name if self.city else 'NoCity'}"


class PropertyImage(Model):
    property = ForeignKey(Property, related_name='images', on_delete=CASCADE)
    image = ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property_id}"
