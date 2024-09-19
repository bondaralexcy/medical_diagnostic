from django.urls import path
from django.views.decorators.cache import cache_page

from services.apps import ServiceConfig
from services.views import ServiceCreateView, ServiceDetailView, ServiceUpdateView, ServiceDeleteView, \
    ContactView, ServiceListView, FeedbackView, SitemapView

app_name = ServiceConfig.name

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('main/', ServiceListView.as_view(), name='service_main'),
    path('create/', ServiceCreateView.as_view(), name='service_form'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('<int:pk>/update/', ServiceUpdateView.as_view(), name='service_update'),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name='service_confirm_delete'),
    path('contact/', ContactView.as_view(), name="contact_list"),
    path('feedback/', FeedbackView.as_view(), name="feedback_list"),
    path('site_map/', SitemapView.as_view(), name="site_map_list"),
]
