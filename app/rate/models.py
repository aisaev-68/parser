from django.db import models


class Rate(models.Model):
    """
    Класс моделили тарифных планов МТС.
    """
    card_title = models.CharField(max_length=200, help_text="Тарифный план")
    card_description = models.TextField(help_text="Описание карточки")
    internet = models.CharField(max_length=50, blank=True, null=True, help_text="Интернет")
    calls = models.CharField(max_length=50, blank=True, null=True, help_text="Звонки")
    speed = models.CharField(max_length=50, blank=True, null=True, help_text="Скорость")
    tv = models.CharField(max_length=50, blank=True, null=True, help_text="ТВ")
    price_main = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name="Цена (основная)")
    price_sale = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, verbose_name="Цена (старая)")
    annotate_price = models.TextField(blank=True, null=True, help_text="Аннотация к цене")
    price_quota = models.CharField(max_length=10, help_text="Валюта")

    def __str__(self):
        return self.card_title

    class Meta:
        verbose_name = "Тарифный план"
        verbose_name_plural = "Тарифные планы"
