from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.models import Patient, Appoint, Result, Doctor


class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Patient
    fields = ['first_name', 'last_name', 'phone', 'address', 'email', 'birth_date', 'created_at']
    template_name = 'main/patient_list.html'
    permission_required = 'main.view_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    success_url = reverse_lazy('main/patient_list')

    def get_queryset(self):
        return Patient.objects.all()


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'main/patient_detail.html'
    success_url = reverse_lazy('main:patient_list.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_item = self.get_object()
        context['title'] = patient_item.name
        return context

    def get_queryset(self):
        return Patient.objects.filter(id=self.kwargs['pk'])


class PatientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Patient
    fields = '__all__'
    template_name = 'main/patient_form.html'
    success_url = reverse_lazy('main:patient_list.html')
    permission_required = 'main.add_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сведения о пациенте'
        return context

    def form_valid(self, form):
        patient = form.save()
        user = self.request.user
        patient.owner = user
        patient.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Patient.objects.all()


class PatientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Patient,
    fields = '__all__'
    template_name = 'main/patient_form.html'
    success_url = reverse_lazy('main:patient_list.html')
    permission_required = 'main.change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_item = self.get_object()
        context['title'] = patient_item.name
        return context

    def get_queryset(self):
        return Patient.objects.filter(id=self.kwargs['pk'])


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'main/patient_confirm_delete.html'
    success_url = reverse_lazy('main:patient_list.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_item = self.get_object()
        context['title'] = patient_item.name
        return context


class AppointListView(ListView):
    model = Appoint
    fields = '__all__'
    template_name = 'main/appoint_list.html'
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.view_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи пациента'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class AppointCreateView(CreateView):
    model = Appoint
    fields = '__all__'
    template_name = 'main/appoint_form.html'
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.add_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Новая запись для пациента'
        return context

    def get_queryset(self):
        return Appoint.objects.all()


class AppointDetailView(DetailView):
    model = Appoint
    template_name = 'main/appoint_detail.html'
    success_url = reverse_lazy('main:appoint_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Запись пациента {appoint_item.patient.last_name} {appoint_item.patient.first_name}'
        return context

    def get_queryset(self):
        return Appoint.objects.filter(id=self.kwargs['pk'])


class AppointUpdateView(UpdateView):
    model = Appoint
    fields = '__all__'
    template_name = 'main/appoint_form.html'
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.change_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Редактирование записи пациента {appoint_item.patient.last_name} {appoint_item.patient.first_name}'
        return context


class AppointDeleteView(DeleteView):
    model = Appoint
    template_name = 'main/appoint_confirm_delete.html'
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.delete_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Отмена записи пациента {appoint_item.patient.last_name} {appoint_item.patient.first_name}'
        return context


class ResultListView(ListView):
    model = Result
    fields = '__all__'
    template_name = 'main/result_list.html'
    success_url = reverse_lazy('services:service_list')
    permission_required = 'main.view_result'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Диагностика'
        return context


class DoctorListView(ListView):
    model = Doctor
    fields = ['name', 'specialization', 'qualification']
    template_name = 'doctor/doctor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    success_url = reverse_lazy('doctor: doctor_list')

    def get_template_names(self):
        if self.request.path == '/doctor/':
            return ['doctor/our_doctors.html']
        elif self.request.path == '/':
            return ['doctor/doctor_list.html']


class DoctorCreateView(CreateView):
    model = Doctor
    fields = ['name', 'specialization', 'qualification']
    template_name = 'doctor/doctor_form.html'
    success_url = reverse_lazy('doctor:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset =Doctor.objects.all(*args, **kwargs)
        return queryset


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor/doctor_detail.html'


class DoctorUpdateView(UpdateView):
    model = Doctor
    fields = ['name', 'specialization', 'qualification']
    template_name = 'doctor/doctor_form.html'
    success_url = reverse_lazy('doctor:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'doctor/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor:doctor_list')


class OurDoctorView(ListView):
    model = Doctor
    template_name = 'doctor/our_doctor.html'

