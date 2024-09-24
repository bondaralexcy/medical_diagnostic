from django.db.models import BooleanField
from django.forms import ModelForm
from main.models import Patient, Appoint, Doctor, Result


class StyleFormMixin:
    """Стилизация форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Добавляем чек-боксы для логических полей
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class PatientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Patient
        exclude = ("owner",)


class PatientModeratorForm(StyleFormMixin, ModelForm):
    """Специальная форма для модератора сайта"""

    class Meta:
        model = Patient
        fields = ("email", "photo", "birth_date")


class AppointForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Appoint
        fields = ("patient", "doctor", "appoint_date")



class DoctorForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"


class ResultForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Result
        exclude = ("date",)
