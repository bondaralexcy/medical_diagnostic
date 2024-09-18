from django.db.models import BooleanField
from django.forms import ModelForm
from main.models import Patient, Appoint, Doctor
from django.utils import timezone
from django.core.exceptions import ValidationError

class StyleFormMixin:
    """ Стилизация форм """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Добавляем чек-боксы для логических полей
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class PatientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Patient
        exclude = ("owner",)


class AppointForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Appoint
        fields = ("patient", "doctor", "appoint_date")

    def clean_appoint_date(self):
        """ Проверка даты. Почему-то не работает"""
        app_date = self.cleaned_data["appoint_date"]
        # current_date = timezone.now()
        # timedelta = int(app_date.day - current_date.day)
        # if timedelta < 0:
        #     raise ValidationError("Invalid date")
        # return app_date

        return app_date

class DoctorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

