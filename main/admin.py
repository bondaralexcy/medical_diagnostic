from django.contrib import admin

from main.models import Patient, Appoint, Result, Doctor


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "last_name",
        "first_name",
        "phone",
        "email",
        "address",
        "birth_date",
        "created_at",
    ]
    list_filter = ("last_name",)
    search_fields = ("last_name", "first_name")


@admin.register(Appoint)
class AppointAdmin(admin.ModelAdmin):
    list_display = ["pk", "patient", "appoint_date", "doctor"]
    list_filter = ("patient",)
    search_fields = ("patient", "appoint_date")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "patient",
        "medical_test",
        "test_result",
        "units_of_measurement",
        "reference_value",
    ]
    list_filter = ("patient",)
    search_fields = ("patient", "medical_test")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["pk", "name", "specialization", "qualification", "experience"]
    list_filter = ("name",)
    search_fields = ("name", "specialization")
