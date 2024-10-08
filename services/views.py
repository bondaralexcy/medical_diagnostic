from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from services.models import Service, Contact, About
from services.forms import ServiceForm

class ServiceListView(ListView):
    model = Service
    fields = ["id", "name", "description", "price"]


class ServiceCreateView(CreateView):
    model = Service
    fields = "__all__"
    form_class = ServiceForm
    success_url = reverse_lazy("services:service_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Создание услуги"
        return context

    def form_valid(self, form):
        return super().form_valid(form)


class ServiceDetailView(DetailView):
    model = Service


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Подробнее о услуге"
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = Service.objects.filter(id=self.kwargs["pk"])
        return queryset


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    # fields = "__all__"
    success_url = reverse_lazy("services:service_list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование услуги"
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset = Service.objects.all(*args, **kwargs)
        return queryset


class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy("services:service_list")



class AboutListView(ListView):
    model = About
    fields = "__all__"


class ContactsPageViews(CreateView):
    """Сохранить информацию о контакте"""

    model = Contact
    fields = (
        "name",
        "phone",
        "message",
    )
    success_url = reverse_lazy("services:contact")
    template_name = "services/contact.html"
    extra_context = {"title": "Сохранить контакт"}


