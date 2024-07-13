from django.db import models


class Category(models.Model):
    category = models.CharField(
        max_length=50,
        verbose_name="Наименование категории",
        help_text="Введите категорию товара",
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True,
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
        help_text="Введите наименование товара",
    )
    description = models.TextField(
        verbose_name="Описание товара",
        blank=True,
        null=True,
        help_text="Введите описание товара",
    )
    image = models.ImageField(
        upload_to="catalog/images/",
        blank=True,
        null=True,
        verbose_name="Фото товара",
        help_text="Загрузите фото товара",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    price = models.FloatField(verbose_name="Цена", help_text="Введите цену товара")
    create_at = models.DateField(verbose_name="Дата поступления товара", auto_now=True)
    update_at = models.DateField(
        verbose_name="Дата изменения данных о товаре", auto_now_add=True
    )
    view_count = models.PositiveIntegerField(verbose_name="Количество просмотров", default=0)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["category", "name", "price"]

    def __str__(self):
        return f"Товар: {self.name}, Категория: {self.category}, Цена: {self.price}"
