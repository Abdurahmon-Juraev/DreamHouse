from apps.models import City, District, Property, PropertyImage, ResidentialComplex, User
from apps.models.property import Like
from apps.models.users import UserProfile
from django.contrib import admin
from django.contrib.admin import TabularInline


class PropertyImageAdmin(TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageAdmin]


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ResidentialComplex)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Like)
