from django.db import models
from users.models import User

NULLABLE = {"null": True, "blank": True}


class Patient(models.Model):
    """Модель для хранения информации о пациентах"""

    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Отчество",
        **NULLABLE,
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        **NULLABLE,
    )
    address = models.CharField(
        max_length=200,
        verbose_name="Адрес",
        **NULLABLE,
    )
    email = models.EmailField(
        verbose_name="Почта",
        **NULLABLE,
    )
    birth_date = models.DateField(
        verbose_name="Дата рождения",
        **NULLABLE,
    )
    photo = models.ImageField(
        upload_to="patient/",
        **NULLABLE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
    )
    owner = models.ForeignKey(
        User,
        default=True,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.surname}"

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
        ordering = ["last_name"]
        permissions = [
            ("can_edit_email", "Can Edit Patient eMail"),
            ("can_edit_photo", "Can Edit Patient Photo"),
            ("can_edit_birthday", "Can Edit Patient Birthday"),
        ]


class Doctor(models.Model):
    """Модель для хранения информации о врачах"""

    name = models.CharField(
        max_length=100,
        verbose_name="ФИО врача",
    )
    specialization = models.CharField(
        max_length=500,
        verbose_name="Специализация",
    )
    qualification = models.CharField(
        max_length=500,
        verbose_name="Квалификация",
        **NULLABLE,
    )
    experience = models.PositiveIntegerField(
        verbose_name="Стаж",
        **NULLABLE,
    )
    education = models.TextField(
        verbose_name="Образование",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="doctor/",
        **NULLABLE,
    )
    comment = models.TextField(
        verbose_name="Комментарии",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        ordering = ["name", "specialization"]
        permissions = [
            ("can_edit_name", "Can Edit Doctor Name"),
            ("can_edit_specialization", "Can Edit Specialization"),
            ("can_edit_avatar", "Can Edit Doctor Avatar"),
        ]


class Appoint(models.Model):
    """Модель для хранения информациио записи пациентов на прием"""

    patient = models.ForeignKey(
        Patient,
        related_name="patients",
        on_delete=models.CASCADE,
        verbose_name="Пациент",
    )
    appoint_date = models.DateTimeField(
        verbose_name="Дата приема врача",
        **NULLABLE,
    )
    doctor = models.ForeignKey(
        Doctor,
        related_name="doctors",
        max_length=100,
        on_delete=models.CASCADE,
        verbose_name="Врач",
    )
    owner = models.ForeignKey(
        User,
        default=True,
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


class Result(models.Model):
    """Модель для хранения результатов обследования"""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name="Пациент",
    )
    date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата исследования",
    )
    medical_test = models.CharField(
        max_length=200,
        verbose_name="Название исследования",
    )
    test_result = models.CharField(
        max_length=150,
        verbose_name="Результат",
    )
    units_of_measurement = models.CharField(
        max_length=100,
        verbose_name="Единицы измерения",
        **NULLABLE,
    )
    reference_value = models.CharField(
        max_length=100,
        verbose_name="Референсное значение",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        ordering = ["-date"]
        permissions = [
            ("can_edit_test_name", "Can Edit Result Name"),
            ("can_edit_test_date", "Can Edit Result Date"),
        ]

    def __str__(self):
        return (
            f"Пациент {self.patient.last_name}, Исследование: {self.medical_test}, "
            f"Результат: {self.test_result}, Референсное значение: {self.reference_values}"
        )
