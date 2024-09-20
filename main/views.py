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
from django.shortcuts import render, get_object_or_404

from main.forms import PatientForm, AppointForm, DoctorForm, PatientModeratorForm, ResultForm
from main.models import Patient, Appoint, Result, Doctor
from main.services import get_doctor_from_cache

def index(request):
    return render(request, "main/index.html")

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


class PatientCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечает за создание записи о пациенте

    Стандартное название шаблона:
    <app_name>/<model_name>_form.html
    """
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy('main:patient_list')


class PatientUpdateView(LoginRequiredMixin, UpdateView):
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

    def get_form_class(self):
        """ Выбор формы в зависимости от прав доступа"""
        user = self.request.user
        if user == self.object.owner:
            return PatientForm
        if user.has_perm("main.can_edit_email") and \
            user.has_perm("main.can_edit_photo") and \
            user.has_perm("main.can_edit_birthday"):
            return PatientModeratorForm
        raise PermissionDenied


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечает за удаление информации о пациенте

    Стандартное название шаблона:
    <app_name>/<model_name>_confirm_delete.html
    """
    model = Patient
    success_url = reverse_lazy('main:patient_list')
    permission_required = 'main.delete_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient_item = self.get_object()
        context['title'] = patient_item.last_name
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied

class AppointListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечает за отображение записей пациентов
    """
    model = Appoint
    fields = ['patient', 'doctor']
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.view_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи пациента'
        return context

    def get_queryset(self, queryset=None):
        """ Запись на прием видит только тот, кто ее создал или модератор"""
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='moderator'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class AppointCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечает за создание записей пациентов
    """
    model = Appoint
    form_class = AppointForm
    fields = ['patient', 'doctor', 'appoint_date']
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.add_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Новая запись для пациента'
        return context

    def get_queryset(self):
        return Appoint.objects.all()


class AppointDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечает за отображение детальной информации о записи пациента
    """
    model = Appoint
    success_url = reverse_lazy('main:appoint_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Запись пациента {appoint_item.patient.last_name} {appoint_item.patient.first_name}'
        return context

    def get_queryset(self):
        return Appoint.objects.filter(id=self.kwargs['pk'])


class AppointUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечает за внесение изменений в записеи пациентов
    """
    model = Appoint
    fields = ['appoint_date', 'doctor']
    form_class = AppointForm
    permission_required = 'main.change_appoint'

    def get_success_url(self):
        return reverse('main:appoint_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Редактирование записи пациента {appoint_item.patient.last_name} {appoint_item.patient.first_name}'
        return context


class AppointDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечает за удаление записей пациентов
    """
    model = Appoint
    success_url = reverse_lazy('main:appoint_list')
    permission_required = 'main.delete_appoint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appoint_item = self.get_object()
        context['title'] = f'Пациент: {appoint_item.patient.last_name} {appoint_item.patient.first_name} {appoint_item.patient.surname}'
        return context


class DoctorListView(ListView):
    """
    Контроллер отвечает за отображение списка врачей
    Стандартное название шаблона:
    <app_name>/<model_name>_<action>.html
    в нашем случае:
    main/doctor_list.html
    """
    model = Doctor
    # Оганичим перечень отображаемых полей
    # Остальные в DetailView
    fields = ['name', 'specialization', 'qualification']
    permission_required = 'main.view_doctor'

    def get_queryset(self):
        # Получим список врачей из кэша
        return get_doctor_from_cache()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    success_url = reverse_lazy('main:doctor_list')


class DoctorCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер отвечает за внесение информации о врачах

    """
    model = Doctor
    form_class = DoctorForm
    success_url = reverse_lazy('main:doctor_list')
    permission_required = 'main.add_doctor'


class DoctorDetailView(DetailView):
    """
    Контроллер отвечает за отображение детальной информации о враче
    """
    model = Doctor


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер отвечает за изменение сведений о враче

    Стандартное название шаблона:
    <app_name>/<model_name>_form.html
    """
    model = Doctor
    form_class = DoctorForm
    permission_required = 'main.change_doctor'

    def get_success_url(self):
        """ Определяем переход при удачном завершении"""
        return reverse('main:doctor_detail', args=[self.kwargs.get('pk')])

class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер отвечает за удаление врача из списка
    Стандартное название шаблона:
    <app_name>/<model_name>_confirm_delete.html
    """
    model = Doctor
    success_url = reverse_lazy('main:doctor_list')
    permission_required = 'main.delete_doctor'

class ResultListView(LoginRequiredMixin, ListView):
    """
    Контроллер отвечает за отображение результатов обследования
    """
    model = Result
    success_url = reverse_lazy('services:service_list')
    permission_required = 'main.view_result'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты обследования'
        return context

class ResultCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер, который отвечает за создание результата
    """
    model = Result
    form_class = ResultForm
    success_url = reverse_lazy('main:result_list')


class ResultUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер, который отвечает за редактирование результата
    """
    model = Result
    form_class = ResultForm
    success_url = reverse_lazy('main:result_list')


class ResultDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер, который отвечает за удаление результатов
    """
    model = Result
    success_url = reverse_lazy('main:result_list')


class ResultDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер отвечает за отображение детальной информации
    о результатах обследования
    """
    model = Result

