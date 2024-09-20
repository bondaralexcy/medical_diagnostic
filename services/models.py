from django.db import models

NULLABLE = {"blank": True, "null": True}


class Service(models.Model):
    service_name = models.CharField(max_length=250, verbose_name="Услуга")
    description = models.TextField(max_length=250, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["service_name"]
        permissions = [
            ("can_add_service", "Может добавлять услугу"),
            ("can_change_service", "Может изменять услугу"),
            ("can_view_service", "Может просматривать услугу"),
        ]


class Contact(models.Model):
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=250, verbose_name="Адрес")

    def __str__(self):
        return f"{self.phone} {self.address} {self.email}"

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["phone"]
