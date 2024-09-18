from django.db import models
from users.models import User

NULLABLE = {"null": True, "blank": True}


class Patient(models.Model):
    """Модель для хранения информации о пациентах"""

    first_name = models.CharField(max_length=100, verbose_name="Имя",)
    surname = models.CharField(max_length=100, verbose_name="Отчество", **NULLABLE,)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия",)
    phone = models.CharField(max_length=20, verbose_name="Телефон",)
    address = models.CharField(max_length=200, verbose_name="Адрес",)
    email = models.EmailField(verbose_name="Почта",)
    birth_date = models.DateField(verbose_name="Дата рождения",)
    photo = models.ImageField(upload_to="patient/", **NULLABLE,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан",)
    owner = models.ForeignKey(
        User, default=True, on_delete=models.CASCADE, verbose_name="Пользователь",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.surname}"

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
        ordering = ["last_name"]


class Doctor(models.Model):
    """Модель для хранения информации о врачах"""

    name = models.CharField(max_length=100, verbose_name="ФИО врача",)
    specialization = models.CharField(max_length=500, verbose_name="Специализация",)
    qualification = models.CharField(max_length=500, verbose_name="Квалификация",)
    experience = models.PositiveIntegerField(verbose_name="Стаж",)
    education = models.TextField(verbose_name="Образование", **NULLABLE,)
    avatar = models.ImageField(upload_to="doctor/", **NULLABLE,)
    comment = models.TextField(verbose_name="Комментарии", **NULLABLE,)

    def __str__(self):
        return f"{self.name} {self.specialization}"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ["name", "specialization"]


class Appoint(models.Model):
    """Модель для хранения информациио записи пациентов на прием"""

    patient = models.ForeignKey(
        Patient,
        related_name="patients",
        on_delete=models.CASCADE,
        verbose_name="Пациент",
    )
    appoint_date = models.DateTimeField(verbose_name="Дата приема врача", **NULLABLE,)
    doctor = models.ForeignKey(
        Doctor,
        related_name="doctors",
        max_length=100,
        on_delete=models.CASCADE,
        verbose_name="Врач",
    )
    owner = models.ForeignKey(
        User, default=True,
        on_delete=models.CASCADE,
        verbose_name="Администратор",
    )

    def __str__(self):
        return (
            f"Пациент {self.patient.last_name} {self.patient.first_name} {self.patient.surname} "
            f"записан на прием к врачу {self.doctor} на {self.appoint_date}"
        )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-appoint_date"]
        permissions = [
            ("сan_add_appoint", "Can Add Appoint"),
            ("can_change_appoint", "Can Edit Appoint"),
            ("can_delete_appoint", "Can Delete Appoint"),
        ]


class Result(models.Model):
    """Модель для хранения результатов обследования"""

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, verbose_name="Пациент",
    )
    date = models.DateField(auto_now_add=True, verbose_name="Дата исследования",)
    medical_test = models.CharField(
        max_length=200, verbose_name="Название исследования",
    )
    test_result = models.CharField(max_length=150, verbose_name="Результат",)
    units_of_measurement = models.CharField(
        max_length=100, verbose_name="Единицы измерения", **NULLABLE,
    )
    reference_value = models.CharField(
        max_length=100, verbose_name="Референсное значение", **NULLABLE,
    )

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        ordering = ["-date"]
        permissions = [
            ("can_view_results", "Can View Results"),
        ]

    def __str__(self):
        return (
            f"Пациент {self.patient.last_name}, Исследование: {self.medical_test}, "
            f"Результат: {self.test_result}, Референсное значение: {self.reference_values}"
        )
