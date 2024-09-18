from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from main.forms import PatientForm, AppointForm, DoctorForm
from main.models import Patient, Appoint, Result, Doctor
from django.shortcuts import render, get_object_or_404


class PatientListView(ListView):
    """
    Контроллер отвечает за отображение списка пациентов

    Стандартное название шаблона:
    <app_name>/<model_name>_<action>.html
    в нашем случае:
    main/patient_list.html

    Создается стандартный контент, который передается в шаблон:
    context = {"object_list: patients}
    """
    model = Patient


class PatientDetailView(DetailView):
    """
    Контроллер отвечает за отображение детальной информации о пациенте
    """
    model = Patient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_item = self.get_object()
        context['title'] = patient_item.last_name
        return context


class PatientCreateView(CreateView):
    """
    Контроллер отвечает за создание записи о пациенте

    Стандартное название шаблона:
    <app_name>/<model_name>_form.html
    """
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('main:patient_list')


class PatientUpdateView(UpdateView):
    """
    Контроллер отвечает за изменение сведений о пациенте

    Стандартное название шаблона:
    <app_name>/<model_name>_form.html
    """
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('main:patient_list')

    def get_success_url(self):
        return reverse('main:patient_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        """ Модифицируем метод get_context_data
            для передачи в форму переменной 'title'
            и создания формсета PatientFormset для записи пациента к врачам
        """

        # Заполняем словарь context_data
        context_data = super().get_context_data(**kwargs)
        patient_item = self.get_object()
        # Добавляем элемент "title"
        context_data["title"] = patient_item.last_name + " " + patient_item.first_name + " " + patient_item.surname
        # Создаем формсет для записей к врачам
        PatientFormset = inlineformset_factory(Patient, Appoint, AppointForm, extra=3)
        if self.request.method == "POST":
            # В случае, если обновляем данные
            context_data["formset"] = PatientFormset(self.request.POST, instance=self.object)
        else:
            # в случае, если просто отображаем
            context_data["formset"] = PatientFormset(instance=self.object)
        return context_data


    def form_valid(self, form):
        """ Переопределяем метод form_valid
            для заполнения поля patient.owner
            и сохранения данных из formset
        """
        context_data = self.get_context_data()
        user = self.request.user
        formset = context_data["formset"]
        # Проверяем на валидность
        if form.is_valid() and formset.is_valid():
            patient = form.save()
            # Добавляем пользователя
            patient.owner = user
            # Сохраняем форму и формсет
            patient.save()
            formset.instance = patient
            formset.save()
            return super().form_valid(form)

        else:
            return render(self.request, self.get_context_data(form=form, formset=formset))





class PatientDeleteView(DeleteView):
    """
    Контроллер отвечает за удаление информации о пациенте

    Стандартное название шаблона:
    <app_name>/<model_name>_confirm_delete.html
    """
    model = Patient
    success_url = reverse_lazy('main:patient_list')


# class Homepage(TemplateView):
#     Model = Patient
#     template_name = "main/base.html"
#     extra_context = {"title": "Медицинская диагностика"}


# class PatientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     """
#     Контроллер отвечает за отображение списка пациентов
#     """
#     model = Patient
#     fields = ['last_name', 'first_name', 'phone', 'email', 'birth_date']
#     template_name = 'main/patient_list.html'
#     extra_context = {"title": "Список пациентов"}
#     permission_required = 'main.view_patient'
#     success_url = reverse_lazy('main:patient_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#
#
#     def get_queryset(self):
#         return Patient.objects.all()


# class PatientDetailView(LoginRequiredMixin, DetailView):
#     """
#     Контроллер отвечает за отображение детальной информации о пациенте
#     """
#     model = Patient
#     fields = ['last_name', 'first_name', 'surname', 'phone', 'address', 'email', 'birth_date']
#     template_name = 'main/patient_detail.html'
#     # extra_context = {"title": "Информация о пациенте"}
#     success_url = reverse_lazy('main:patient_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         patient_item = self.get_object()
#         context['title'] = patient_item.first_name
#         return context

    # def get_queryset(self):
    #     return Patient.objects.filter(id=self.kwargs['pk'])


# class PatientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     """
#     Контроллер отвечает за создание записи о пациенте
#     """
#     model = Patient
#     fields = ['last_name', 'first_name', 'surname', 'phone', 'address', 'email', 'birth_date']
#     template_name = 'main/patient_form.html'
#     # extra_context = {"title": "Новый пациент"}
#     success_url = reverse_lazy('main:patient_list')
#     permission_required = 'main.add_patient'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Новый пациент'
#         return context
#
#     def form_valid(self, form):
#         """ Заполняем поле patient.owner """
#         patient = form.save()
#         user = self.request.user
#         patient.owner = user
#         patient.save()
#         return super().form_valid(form)

    # def get_queryset(self):
    #     return Patient.objects.all()


# class PatientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     """
#     Контроллер отвечает за изменение сведений о пациенте
#     """
#     model = Patient,
#     fields = ['last_name', 'first_name', 'surname', 'phone', 'address', 'email', 'birth_date']
#     template_name = 'main/patient_form.html'
#     success_url = reverse_lazy('main:patient_list')
#     permission_required = 'main.change_patient'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         patient_item = self.get_object()
#         context['title'] = patient_item.last_name
#         return context
#
#     def get_queryset(self):
#         return Patient.objects.filter(id=self.kwargs['pk'])


# class PatientDeleteView(LoginRequiredMixin, DeleteView):
#     """
#     Контроллер отвечает за удаление информации о пациенте
#     """
#     model = Patient
#     template_name = 'main/patient_confirm_delete.html'
#     success_url = reverse_lazy('main:patient_list')
#     permission_required = 'main.delete_patient'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         patient_item = self.get_object()
#         context['title'] = patient_item.last_name
#         return context
#
#     def get_object(self, queryset=None):
#         self.object = super().get_object(queryset)
#         if self.request.user == self.object.owner or self.request.user.is_superuser:
#             return self.object
#         raise PermissionDenied

class AppointListView(ListView):
    """
    Контроллер отвечает за отображение записей пациентов
    """
    model = Appoint
    fields = ['patient', 'doctor']
    template_name = 'main/appoint_list.html'
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.view_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи пациента'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class AppointCreateView(CreateView):
    """
    Контроллер отвечает за создание записей пациентов
    """
    model = Appoint
    fields = ['patient', 'doctor', 'appoint_date']
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
    """
    Контроллер отвечает за отображение детальной информации о записи пациента
    """
    model = Appoint
    # fields = ['patient', 'record_date', 'record_time', 'doctor']
    fields = '__all__'
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
    """
    Контроллер отвечает за внесение изменений в записеи пациентов
    """
    model = Appoint
    fields = ['appoint_date', 'doctor']
    template_name = 'main/appoint_form.html'
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.change_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Редактирование записи пациента {appoint_item.patient.last_name} {appoint_item.patient.first_name}'
        return context


class AppointDeleteView(DeleteView):
    """
    Контроллер отвечает за удаление записей пациентов
    """
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
    """
    Контроллер отвечает за отображение результатов обследования
    """
    model = Result
    fields = '__all__'
    template_name = 'main/result_list.html'
    success_url = reverse_lazy('services:service_list')
    permission_required = 'main.view_result'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты обследования'
        return context


class DoctorListView(ListView):
    """
    Контроллер отвечает за отображение списка врачей
    """
    model = Doctor
    fields = ['name', 'specialization', 'qualification']
    template_name = 'main/doctor_list.html'
    permission_required = 'main.view_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    success_url = reverse_lazy('main:doctor_list')

    # def get_template_names(self):
    #     if self.request.path == '/doctor/':
    #         return ['main/our_doctors.html']
    #     elif self.request.path == '/':
    #         return ['main/doctor_list.html']


class DoctorCreateView(CreateView):
    """
    Контроллер отвечает за внесение информации о врачах
    """
    model = Doctor
    fields = ['name', 'specialization', 'qualification']
    template_name = 'main/doctor_form.html'
    success_url = reverse_lazy('main:doctor_list')
    permission_required = 'main.add_doctor'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset =Doctor.objects.all(*args, **kwargs)
        return queryset


class DoctorDetailView(DetailView):
    """
    Контроллер отвечает за отображение детальной информации о враче
    """
    model = Doctor
    fields = '__all__'
    template_name = 'main/doctor_detail.html'


class DoctorUpdateView(UpdateView):
    """
    Контроллер отвечает за изменение информации о враче
    """
    model = Doctor
    fields = ['name', 'specialization', 'qualification']
    template_name = 'main/doctor_form.html'
    success_url = reverse_lazy('main:doctor_list')
    permission_required = 'main.change_doctor'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DoctorDeleteView(DeleteView):
    """
    Контроллер отвечает за удаление врача из списка
    """
    model = Doctor
    template_name = 'main/doctor_confirm_delete.html'
    success_url = reverse_lazy('main:doctor_list')
    permission_required = 'main.delete_doctor'


class OurDoctorView(ListView):
    """
    Контроллер отвечает за альтернативное отображение данных о враче
    """
    model = Doctor
    template_name = 'main/our_doctor.html'

