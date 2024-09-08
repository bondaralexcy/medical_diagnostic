from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from services.models import Service, Contact, Sitemap


class ServiceListView(ListView):
    model = Service
    fields = ['id', 'name', 'description', 'price']
    paginate_by = 10
    permission_required = 'services.view_service'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Все услуги'
        return context

    def get_template_names(self):
        if self.request.path == '/':
            return ['services/service_list.html']
        elif self.request.path == '/services/':
            return ['services/service_main.html']


class ServiceCreateView(CreateView):
    model = Service
    fields = '__all__'
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:service_list')
    permission_required = 'services.add_service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Создание услуги'
        return context

    def form_valid(self, form):
        return super().form_valid(form)


class ServiceDetailView(DeleteView):
    model = Service
    template_name = 'services/service_detail.html'
    success_url = reverse_lazy('services:service_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подробнее о услуге'
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = Service.objects.filter(id=self.kwargs['pk'])
        return queryset


class ServiceUpdateView(UpdateView):
    model = Service
    fields = '__all__'
    template_name = 'services/service_form.html'
    success_url = reverse_lazy('services:service_list')
    permission_required = 'services.change_service'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование услуги'
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self, *args, **kwargs):
        queryset = Service.objects.all(*args, **kwargs)
        return queryset


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'services/service_confirm_delete.html'
    success_url = reverse_lazy('services:service_list')


class ContactView(ListView):
    model = Contact
    fields = '__all__'
    template_name = 'services/contact_list.html'


class FeedbackView(ListView):
    model = Contact
    fields = '__all__'
    template_name = 'services/feedback_list.html'


class SitemapView(ListView):
    model = Sitemap
    fields = '__all__'
    template_name = 'services/site_map_list.html'
