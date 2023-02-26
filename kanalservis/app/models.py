from django.db import models


class Order(models.Model):
    ord_id = models.PositiveIntegerField(
        verbose_name="№",
        unique=True,
    )
    ord_num = models.PositiveIntegerField(
        verbose_name="Заказ №",
        unique=True,
    )
    ord_cost = models.FloatField(
        verbose_name="Стоимость,$",
    )
    ord_date = models.DateField(
        verbose_name="Срок поставки",
    )
    ord_cost_rub = models.FloatField(verbose_name="Стоимость, руб.", null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return str(self.ord_id)
