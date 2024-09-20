from django.test import TestCase

from main.models import Doctor, Appoint, Result, Patient
from services.models import Service
from users.models import User


class DoctorTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.doctor = Doctor.objects.create(
            name="Иванов Иван Иванович", specialization="Хирург"
        )

    def test_doctor_detail(self):
        doctor = Doctor.objects.get(name="Иванов Иван Иванович")
        self.assertEqual(doctor.specialization, "Хирург")

    def test_doctor_list(self):
        doctors_count = Doctor.objects.all().count()
        self.assertEqual(doctors_count, 1)

    def test_doctor_update(self):
        doctor = Doctor.objects.get(name="Иванов Иван Иванович")
        doctor.specialization = "ЛОР"
        self.assertEqual(doctor.specialization, "ЛОР")

    def test_doctor_create(self):
        Doctor.objects.create(name="Петров Петр Петрович", specialization="ЛОР")
        doctors_count = Doctor.objects.all().count()
        self.assertEqual(doctors_count, 2)

    def test_doctor_delete(self):
        doctor = Doctor.objects.get(name="Иванов Иван Иванович")
        doctor.delete()
        doctors_count = Doctor.objects.all().count()
        self.assertEqual(doctors_count, 0)


class ServiceTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.service = Service.objects.create(service_name="УЗИ", price=2000)

    def test_service_detail(self):
        service = Service.objects.get(service_name="УЗИ")
        self.assertEqual(service.price, 2000)

    def test_service_list(self):
        services_count = Service.objects.all().count()
        self.assertEqual(services_count, 1)

    def test_service_update(self):
        service = Service.objects.get(service_name="УЗИ")
        service.price = 1500
        self.assertEqual(service.price, 1500)

    def test_service_create(self):
        self.service = Service.objects.create(service_name="КТ", price=5000)
        services_count = Service.objects.all().count()
        self.assertEqual(services_count, 2)

    def test_service_delete(self):
        service = Service.objects.get(service_name="УЗИ")
        service.delete()
        services_count = Service.objects.all().count()
        self.assertEqual(services_count, 0)


class AppointTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.doctor = Doctor.objects.create(
            name="Иванов Иван Иванович", specialization="Хирург"
        )
        self.patient = Patient.objects.create(
            first_name="Петр", last_name="Кузнецов", owner=self.user
        )
        self.appoint = Appoint.objects.create(
            patient=self.patient,
            appoint_date="2024-09-20 12:00",
            doctor=self.doctor,
            owner=self.user,
        )

    def test_appoint_detail(self):
        appoint = Appoint.objects.get(owner=self.user)
        self.assertEqual(appoint.doctor.name, "Иванов Иван Иванович")

    def test_appoint_list(self):
        appoint_count = Appoint.objects.all().count()
        self.assertEqual(appoint_count, 1)

    def test_appoint_update(self):
        appoint = Appoint.objects.get(owner=self.user)
        appoint.doctor.name = "Петров Петр Петрович"
        self.assertEqual(appoint.doctor.name, "Петров Петр Петрович")

    def test_appoint_create(self):
        self.appoint = Appoint.objects.create(
            patient=self.patient,
            appoint_date="2024-10-20 12:00",
            doctor=self.doctor,
            owner=self.user,
        )
        appoint_count = Appoint.objects.all().count()
        self.assertEqual(appoint_count, 2)

    def test_appoint_delete(self):
        appoint = Appoint.objects.get(owner=self.user)
        appoint.delete()
        appoint_count = Appoint.objects.all().count()
        self.assertEqual(appoint_count, 0)


class ResultTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.patient = Patient.objects.create(
            first_name="Петр", last_name="Кузнецов", owner=self.user
        )
        self.result = Result.objects.create(
            patient=self.patient, medical_test="СОЭ", test_result="24"
        )

    def test_result_detail(self):
        result = Result.objects.get(medical_test="СОЭ")
        self.assertEqual(result.test_result, "24")

    def test_result_list(self):
        results_count = Result.objects.all().count()
        self.assertEqual(results_count, 1)

    def test_result_update(self):
        result = Result.objects.get(medical_test="СОЭ")
        result.test_result = "15"
        self.assertEqual(result.test_result, "15")

    def test_result_create(self):
        self.patient = Patient.objects.create(
            first_name="Петр", last_name="Кузнецов", owner=self.user
        )
        self.test_result = Result.objects.create(
            patient=self.patient, medical_test="СРБ", test_result="2"
        )
        results_count = Result.objects.all().count()
        self.assertEqual(results_count, 2)

    def test_appointment_delete(self):
        result = Result.objects.get(medical_test="СОЭ")
        result.delete()
        results_count = Result.objects.all().count()
        self.assertEqual(results_count, 0)
