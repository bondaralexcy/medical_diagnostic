from django.urls import path

from services.apps import ServiceConfig
from services.views import (
    ServiceListView,
    ServiceCreateView,
    ServiceDetailView,
    ServiceUpdateView,
    ServiceDeleteView,
    ContactsPageViews,
    AboutListView
)

app_name = ServiceConfig.name

urlpatterns = [
    path("", ServiceListView.as_view(), name="service_list"),
    path("main/", ServiceListView.as_view(), name="service_main"),
    path("create/", ServiceCreateView.as_view(), name="service_form"),
    path("<int:pk>/", ServiceDetailView.as_view(), name="service_detail"),
    path("<int:pk>/update/", ServiceUpdateView.as_view(), name="service_update"),
    path(
        "<int:pk>/delete/", ServiceDeleteView.as_view(), name="service_confirm_delete"
    ),
    path("contact/", ContactsPageViews.as_view(), name="contact_form"),
    path("about/", AboutListView.as_view(), name="about_list"),
]
