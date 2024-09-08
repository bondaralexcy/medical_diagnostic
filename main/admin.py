from django.contrib import admin

from main.models import Client, Record, Diagnostics, Doctor


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'surname', 'phone', 'email', 'address', 'birth_date', 'created_at']


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['pk', 'client', 'record_date', 'record_time', 'doctor']


@admin.register(Diagnostics)
class DiagnosticsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'client', 'diagnosis', 'result', 'test', 'units_of_measurement', 'proper_values']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'patronymic', 'surname', 'specialization', 'qualification', 'experience']