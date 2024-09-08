from django.db.models import BooleanField
from django.forms import ModelForm

from main.models import Patient, Appoint, Doctor


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class PatientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Patient
        fields = ('first_name', 'last_name', 'phone', 'address', 'email', 'birth_date', 'created_at')


class AppointForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Appoint
        fields = ('patient', 'record_date', 'record_time', 'doctor')


class DoctorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Doctor
        fields = ('name', 'specialization', 'qualification', 'experience')
