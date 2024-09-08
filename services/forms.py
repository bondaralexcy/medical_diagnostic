from django.db.models import BooleanField
from django.forms import ModelForm

from services.models import Service, Contact, Sitemap


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ServiceForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'description', 'price')


class ContactForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Contact
        fields = ('email', 'phone', 'address')


class FeedbackForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'content')


class SitemapForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Sitemap
        fields = ('title', 'content', 'travel_map')
