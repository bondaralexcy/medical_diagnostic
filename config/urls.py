from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from services.views import ServiceListView
from main.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("index/", index),
    path("", ServiceListView.as_view(), name="homepage"),
    path("main/", include("main.urls", namespace="main")),
    path("services/", include("services.urls", namespace="services")),
    path("users/", include("users.urls", namespace="users")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
