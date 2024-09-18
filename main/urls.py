from django.urls import path, include
# from django.views.decorators.cache import cache_page

# from main.views import PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView, \
#     AppointListView, AppointCreateView, AppointUpdateView, AppointDeleteView, AppointDetailView, ResultListView, \
#     DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView, OurDoctorView

from main.apps import MainConfig
from main.views import PatientListView, PatientDetailView, PatientCreateView, PatientUpdateView, PatientDeleteView

app_name = MainConfig.name

urlpatterns = [
     path('', PatientListView.as_view(), name='patient_list'),
     path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
     path('patient/create/', PatientCreateView.as_view(), name='patient_create'),
     path('patient/<int:pk>/update/', PatientUpdateView.as_view(), name='patient_update'),
     path('patient/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_confirm_delete'),
]

# urlpatterns = [
#     path('', PatientListView.as_view(), name='patient_list'),
#     path('patient/create/', PatientCreateView.as_view(), name='patient_form'),
#     path('patient/<int:pk>', PatientDetailView.as_view(), name='patient_detail'),
#     path('patient/<int:pk>/update/', PatientUpdateView.as_view(), name='patient_update'),
#     path('patient/<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_confirm_delete'),
#     path('appoint/', AppointListView.as_view(), name='appoint_list'),
#     path('appoint/<int:pk>', AppointDetailView.as_view(), name='appoint_detail'),
#     path('appoint/create/', AppointCreateView.as_view(), name='appoint_form'),
#     path('appoint/<int:pk>/update/', AppointUpdateView.as_view(), name='appoint_update'),
#     path('appoint/<int:pk>/delete/', AppointDeleteView.as_view(), name='appoint_confirm_delete'),
#     path('result/', ResultListView.as_view(), name='result_list'),
#     path('doctor/', DoctorListView.as_view(), name='doctor_list'),
#     path('our_doctors/', OurDoctorView.as_view(), name='our_doctors'),
#     path('doctor/create/', DoctorCreateView.as_view(), name='doctor_form'),
#     path('doctor/<int:pk>/', DoctorDetailView.as_view(), name='doctor_detail'),
#     path('doctor/<int:pk>/update/', DoctorUpdateView.as_view(), name='doctor_update'),
#     path('doctor/<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor_confirm_delete'),
#
# ]
