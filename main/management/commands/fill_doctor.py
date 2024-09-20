from django.core.management import BaseCommand

from doctor.models import Doctor


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        doctor_list = [
            {"name": "Иванов", "specialization": "Хирург", "qualification": "Высшая", "experience": 12, "education": "2-й мед"},
            {"name": "Петров", "specialization": "Терапевт", "qualification": "Высшая", "experience": 12, "education": "2-й мед"},
            {"name": "Сидоров", "specialization": "Онколог", "qualification": "Высшая", "experience": 12, "education": "2-й мед"},
        ]
        doctor_for_create = []
        for doctor_item in doctor_list:
            doctor_for_create.append(**doctor_item)
            Doctor.objects.bulk_create(doctor_for_create)
