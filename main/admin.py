from django.contrib import admin

from main.models import Patient, Appoint, Result, Doctor

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'last_name', 'first_name', 'phone', 'email', 'address', 'birth_date', 'created_at']


@admin.register(Appoint)
class AppointAdmin(admin.ModelAdmin):
    list_display = ['pk', 'patient', 'record_date', 'record_time', 'doctor']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['pk', 'patient', 'medical_test', 'test_result', 'units_of_measurement', 'reference_value']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'specialization', 'qualification', 'experience']