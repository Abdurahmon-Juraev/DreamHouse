from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ImageField,
    IntegerField,
    Model,
    TextField,
)
from django.db.models.enums import TextChoices


class City(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class District(Model):
    city = ForeignKey('apps.City', related_name='districts', on_delete=CASCADE)
    name = CharField(max_length=100)

    def __str__(self):
        return f"{self.name} — {self.city.name}"


class ResidentialComplex(Model):
    name = CharField(max_length=255)
    city = ForeignKey('apps.City', on_delete=SET_NULL, null=True, blank=True)
    address = CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Property(Model):
    class Currency(TextChoices):
        USD = 'usd', 'Dollar'
        UZS = 'uzs', "So'm"

    class TRANSACTION(TextChoices):
        Sale = 'sale', 'Sale'
        Rent = 'rent', 'Rent'

    class PropertyType(TextChoices):
        Apartment = 'Apartment', 'Apartment'
        Land = 'Land', 'Land'
        Office = 'Office', 'Office'
        House = 'House', 'House'
        Residential = 'Residential complex', 'Residential complex'

    class ROOM(TextChoices):
        bir = '1', '1'
        ikki = '2', '2'
        uch = '3', '3'
        tort = '4', '4'
        besh = '5', '5'
        olti = '6', '6'
        yetti = '7', '7'

    title = CharField(max_length=255)
    description = TextField(blank=True)
    agent = ForeignKey('apps.User', related_name='properties', on_delete=SET_NULL, null=True, blank=True)
    property_type = CharField(max_length=50, choices=PropertyType.choices, default=PropertyType.Apartment)
    transaction_type = CharField(max_length=10, choices=TRANSACTION.choices, default=TRANSACTION.Sale)
    price = DecimalField(max_digits=15, decimal_places=2)
    currency = CharField(max_length=3, choices=Currency.choices, default=Currency.UZS)
    region = ForeignKey('apps.City', CASCADE)
    district = ForeignKey('apps.District', CASCADE)
    address = CharField(max_length=255, blank=True, null=True)
    rooms = IntegerField(choices=ROOM.choices, default=ROOM.bir)
    residential_complex = ForeignKey('apps.ResidentialComplex', on_delete=SET_NULL, null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class PropertyImage(Model):
    property = ForeignKey(Property, related_name='images', on_delete=CASCADE)
    image = ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property_id}"


class Like(Model):
    property = ForeignKey(Property, related_name='likes', on_delete=CASCADE)
    user = ForeignKey('apps.User', related_name='likes', on_delete=CASCADE)

    def __str__(self):
        return f"Likes for {self.property}"
