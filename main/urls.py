from django.urls import path, include
from main.apps import MainConfig

from main.views import (
    PatientListView,
    PatientDetailView,
    PatientCreateView,
    PatientUpdateView,
    PatientDeleteView,
)
from main.views import (
    AppointListView,
    AppointCreateView,
    AppointUpdateView,
    AppointDeleteView,
    AppointDetailView,
)
from main.views import (
    DoctorListView,
    DoctorDetailView,
    DoctorCreateView,
    DoctorUpdateView,
    DoctorDeleteView,
)
from main.views import (
    ResultListView,
    ResultDetailView,
    ResultCreateView,
    ResultUpdateView,
    ResultDeleteView,
)

app_name = MainConfig.name

urlpatterns = [
    path("", PatientListView.as_view(), name="patient_list"),
    path("patient/<int:pk>/", PatientDetailView.as_view(), name="patient_detail"),
    path("patient/create/", PatientCreateView.as_view(), name="patient_create"),
    path("patient/<int:pk>/update/", PatientUpdateView.as_view(), name="patient_update"),
    path("patient/<int:pk>/delete/", PatientDeleteView.as_view(),name="patient_confirm_delete",),
    path("appoint/", AppointListView.as_view(), name="appoint_list"),
    path("appoint/<int:pk>", AppointDetailView.as_view(), name="appoint_detail"),
    path("appoint/create/", AppointCreateView.as_view(), name="appoint_form"),
    path("appoint/<int:pk>/update/", AppointUpdateView.as_view(), name="appoint_update"),
    path("appoint/<int:pk>/delete/", AppointDeleteView.as_view(), name="appoint_confirm_delete"),
    path("doctor/", DoctorListView.as_view(), name="doctor_list"),
    path("doctor/<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),
    path("doctor/create/", DoctorCreateView.as_view(), name="doctor_create"),
    path("doctor/<int:pk>/update/", DoctorUpdateView.as_view(), name="doctor_update"),
    path(
        "doctor/<int:pk>/delete/",
        DoctorDeleteView.as_view(),
        name="doctor_confirm_delete",
    ),
    path("result/", ResultListView.as_view(), name="result_list"),
    path("result/<int:pk>/", ResultDetailView.as_view(), name="result_detail"),
    path("result/create/", ResultCreateView.as_view(), name="result_create"),
    path("result/<int:pk>/update/", ResultUpdateView.as_view(), name="result_update"),
    path(
        "result/<int:pk>/delete/",
        ResultDeleteView.as_view(),
        name="result_confirm_delete",
    ),
]
