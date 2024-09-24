from django.db.models import BooleanField
from django.forms import ModelForm

from services.models import Service, Contact


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ServiceForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Service
        fields = ("service_name", "description", "price")


class ContactForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

