from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вещь'
        verbose_name_plural = 'Предметы'
        # permissions = [
        #     ("can_unpublish_product", "Can unpublish product"),
        #     ("can_edit_product_description", "Can edit product description"),
        #     ("can_edit_product_category", "Can edit product category"),
        # ]