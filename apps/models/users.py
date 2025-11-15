from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, BooleanField, CharField, Model, OneToOneField, TextChoices


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone is required")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    phone = CharField(max_length=30, unique=True)
    is_agent = BooleanField(default=False)
    username = None
    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []
    objects = UserManager()


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
