# app/property/py
from django.contrib.auth.models import AbstractUser
from django.db.models import (CASCADE, BooleanField, CharField, Model,
                              OneToOneField, TextChoices)


class User(AbstractUser):
    phone = CharField(max_length=30, unique=True)
    is_agent = BooleanField(default=False)

    username = None

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = ['email']


class UserProfile(Model):
    class UserType(TextChoices):
        Admin = 'admin'
        Private_owner = 'private_owner'
        owner = 'owner'
    user = OneToOneField(User, CASCADE)
    FirstName = CharField(max_length=30, blank=True)
    LastName = CharField(max_length=30, blank=True)
    CompanyName = CharField(max_length=30, blank=True)
    TypeUser = CharField(max_length=15, choices=UserType.choices, default=UserType.Private_owner)



