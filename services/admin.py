from django.contrib import admin
from services.models import Service, Contact


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["pk", "service_name", "description", "price"]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "phone", "message"]
    search_fields = ("name", "phone")
