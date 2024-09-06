from django.db import models
from django.db.models import SET_NULL

from config.settings import NULLABLE
from users.models import User


class Category(models.Model):
    category = models.CharField(
        max_length=50,
        verbose_name="Наименование категории",
        help_text="Введите категорию товара"
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"Категория: {self.category}"


class Product(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите наименование товара"
    )
    description = models.TextField(
        verbose_name="Описание товара",
        **NULLABLE,
        help_text="Введите описание товара"
    )
    image = models.ImageField(
        upload_to="catalog/images/",
        **NULLABLE,
        verbose_name="Фото товара",
        help_text="Загрузите фото товара"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    price = models.FloatField(
        verbose_name="Цена",
        help_text="Введите цену товара")

    create_at = models.DateField(
        verbose_name="Дата поступления товара",
        auto_now=True
    )
    update_at = models.DateField(
        verbose_name="Дата изменения данных о товаре",
        auto_now_add=True
    )
    view_count = models.PositiveIntegerField(
        verbose_name="Количество просмотров",
        default=0
    )

    owner = models.ForeignKey(
        User,
        verbose_name="Продавец",
        help_text='Введите наименование продавца',
        **NULLABLE,
        on_delete=SET_NULL
    )


    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["category", "name", "price"]

    def __str__(self):
        return f"Товар: {self.name}, Категория: {self.category}, Цена: {self.price}"


class ProductVersion(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="продукт",
        related_name='product_versions'
    )

    version_number = models.PositiveIntegerField(
        verbose_name="Номер версии"
    )

    version_name = models.CharField(
        max_length=100,
        verbose_name="Название версии"
    )

    is_current = models.BooleanField(
        verbose_name="Признак текущей версии",
        default=True
    )

    class Meta:
        verbose_name = "Версия продукта"
        verbose_name_plural = "Версии продукта"
        ordering = ["-version_number"]
        unique_together = ["product", "version_number"]

    def __str__(self):
        return (f"Версия продукта: {self.product}, Номер версии: {self.version_number}, "
                f"Название версии: {self.version_name}")
