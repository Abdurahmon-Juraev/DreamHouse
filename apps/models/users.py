# app/property/py
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, OneToOneField, CASCADE, CharField, BooleanField


class User(AbstractUser):
    phone = CharField(max_length=30, blank=True, null=True)
    is_agent = BooleanField(default=False)

    REQUIRED_FIELDS = ['email']
