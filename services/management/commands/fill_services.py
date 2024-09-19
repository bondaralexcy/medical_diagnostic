from django.core.management import BaseCommand

from services.models import Service


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        service_list = [
            {"name": "Service1", "price": 100},
            {"name": "Service2", "price": 200},
            {"name": "Service3", "price": 300},
        ]
        service_for_create = []
        for service_item in service_list:
            service_for_create.append(**service_item)
            Service.objects.bulk_create(service_for_create)