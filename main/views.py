# from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.urls import reverse_lazy
# from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#
# from main.models import Client, Record, Diagnostics
#
#
# class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Client
#     fields = ['name', 'surname', 'phone', 'address', 'email', 'birth_date', 'created_at']
#     template_name = 'health/client_list.html'
#     permission_required = 'health.view_client'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
#     success_url = reverse_lazy('health/client_list')
#
#     def get_queryset(self):
#         return Client.objects.all()
#
#
# class ClientDetailView(LoginRequiredMixin, DetailView):
#     model = Client
#     template_name = 'health/client_detail.html'
#     success_url = reverse_lazy('health:client_list.html')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         client_item = self.get_object()
#         context['title'] = client_item.name
#         return context
#
#     def get_queryset(self):
#         return Client.objects.filter(id=self.kwargs['pk'])
#
#
# class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Client
#     fields = '__all__'
#     template_name = 'health/client_form.html'
#     success_url = reverse_lazy('health:client_list.html')
#     permission_required = 'health.add_client'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Создание клиента'
#         return context
#
#     def form_valid(self, form):
#         client = form.save()
#         user = self.request.user
#         client.owner = user
#         client.save()
#         return super().form_valid(form)
#
#     def get_queryset(self):
#         return Client.objects.all()
#
#
# class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     model = Client,
#     fields = '__all__'
#     template_name = 'health/client_form.html'
#     success_url = reverse_lazy('health:client_list.html')
#     permission_required = 'health.change_client'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         client_item = self.get_object()
#         context['title'] = client_item.name
#         return context
#
#     def get_queryset(self):
#         return Client.objects.filter(id=self.kwargs['pk'])
#
#
# class ClientDeleteView(LoginRequiredMixin, DeleteView):
#     model = Client
#     template_name = 'health/client_confirm_delete.html'
#     success_url = reverse_lazy('health:client_list.html')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         client_item = self.get_object()
#         context['title'] = client_item.name
#         return context
#
#
# class RecordListView(ListView):
#     model = Record
#     fields = '__all__'
#     template_name = 'health/record_list.html'
#     success_url = reverse_lazy('health:record_list')
#     permission_required = 'health.view_record'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = f'Записи клиента'
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = super().get_queryset(*args, **kwargs)
#         queryset = queryset.filter(publication=True)
#         return queryset
#
#
# class RecordCreateView(CreateView):
#     model = Record
#     fields = '__all__'
#     template_name = 'health/record_form.html'
#     success_url = reverse_lazy('health:record_list')
#     permission_required = 'health.add_record'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = f'Создание записи для клиента'
#         return context
#
#     def get_queryset(self):
#         return Record.objects.all()
#
#
# class RecordDetailView(DetailView):
#     model = Record
#     template_name = 'health/record_detail.html'
#     success_url = reverse_lazy('health:record_list')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         record_item = self.get_object()
#         context['title'] = f'Запись клиента {record_item.client.name} {record_item.client.surname}'
#         return context
#
#     def get_queryset(self):
#         return Record.objects.filter(id=self.kwargs['pk'])
#
#
# class RecordUpdateView(UpdateView):
#     model = Record
#     fields = '__all__'
#     template_name = 'health/record_form.html'
#     success_url = reverse_lazy('health:record_list')
#     permission_required = 'health.change_record'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         record_item = self.get_object()
#         context['title'] = f'Редактирование записи клиента {record_item.client.name} {record_item.client.surname}'
#         return context
#
#
# class RecordDeleteView(DeleteView):
#     model = Record
#     template_name = 'health/record_confirm_delete.html'
#     success_url = reverse_lazy('health:record_list')
#     permission_required = 'health.delete_record'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         record_item = self.get_object()
#         context['title'] = f'Удаление записи клиента {record_item.client.name} {record_item.client.surname}'
#         return context
#
#
# class DiagnosticsListView(ListView):
#     model = Diagnostics
#     fields = '__all__'
#     template_name = 'health/diagnostics_list.html'
#     success_url = reverse_lazy('services:service_list')
#     permission_required = 'health.view_diagnostics'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Лечебные консультации'
#         return context
