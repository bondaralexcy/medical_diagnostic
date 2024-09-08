from django.db import models
from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Patient(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    surname = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    email = models.EmailField(verbose_name='Почта')
    birth_date = models.DateField(verbose_name='Дата рождения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.surname}'

    class Meta:
        verbose_name = 'пациент'
        verbose_name_plural = 'пациенты'
        ordering = ['last_name']


class Appoint(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пациент')
    record_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')
    record_time = models.TimeField(verbose_name='Время записи')
    doctor = models.ForeignKey(Doctor, max_length=100, on_delete=models.CASCADE, verbose_name='Врач')
    owner = models.ForeignKey(User, default=True, on_delete=models.CASCADE, verbose_name='Пользователь')
    # publication = models.BooleanField(default=True, verbose_name="Признак публикации")

    def __str__(self):
        return (f'Пациент {self.patient.last_name} {self.patient.first_name} {self.patient.surname} '
                f'записан на прием к врачу {self.doctor} на {self.record_date} в {self.record_time}')

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'
        permissions = [
            ('can_add_record', 'Может добавлять запись'),
            ('can_change_record', 'Может изменять запись'),
            ('can_view_record', 'Может просматривать запись'),
            ('can_delete_record', 'Может удалять запись'),
        ]


class Result(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='Пациент')
    date = models.DateField(auto_now_add=True, verbose_name='Дата исследования')
    medical_test= models.CharField(max_length=200, verbose_name='Название исследования')
    test_result = models.CharField(max_length=150, verbose_name='Результат')
    units_of_measurement = models.CharField(max_length=100, verbose_name='Единицы измерения', **NULLABLE)
    reference_value = models.CharField(max_length=100, verbose_name='Референсное значение', **NULLABLE)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        ordering = ['-date']
        permissions = [
            ('can_view_results', 'Может просматривать результаты исследования'),
        ]

    def __str__(self):
        return (f'Пациент {self.patient.last_name}, Исследование: {self.medical_test}, '
                f'Результат: {self.test_result}, Референсное значение: {self.reference_values}')



class Doctor(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО врача')
    age = models.PositiveIntegerField(verbose_name='Возраст', **NULLABLE)
    specialization = models.CharField(max_length=255, verbose_name='Специализация')
    qualification = models.CharField(max_length=255, verbose_name='Квалификация')
    experience = models.PositiveIntegerField(verbose_name='Стаж')
    education = models.TextField(verbose_name='Образование', **NULLABLE)
    avatar = models.ImageField(upload_to='doctor/', **NULLABLE)
    comment = models.TextField(verbose_name='Дополинительная информация', **NULLABLE)
    def __str__(self):
        return f'{self.name} {self.specialization}'

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'врачи'
        ordering = ['name', 'specialization']


