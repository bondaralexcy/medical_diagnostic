from django.db import models

NULLABLE = {"blank": True, "null": True}


class Service(models.Model):
    service_name = models.CharField(max_length=250, verbose_name="Услуга",)
    description = models.TextField(verbose_name="Описание",)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена",)

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
    """
    Модель для хранения информации о контактах
    """

    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    phone = models.CharField(
        max_length=50,
        verbose_name="Телефон",
        **NULLABLE,
    )
    message = models.TextField(
        verbose_name="Сообщение",
        **NULLABLE,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"



class About(models.Model):
    description = models.TextField(verbose_name="Описание", **NULLABLE,)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Презентация"
        verbose_name_plural = "Презентации"
