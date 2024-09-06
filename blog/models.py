from django.db import models
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from slugify import slugify
from requests import request

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок', help_text='Введите заголовок статьи')
    slug = models.CharField(max_length=200, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержимое статьи', help_text='Введите текст статьи')
    image = models.ImageField(null=True, blank=True, upload_to='blog_images/', verbose_name='Изображение статьи', help_text='Загрузите')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'Статья: {self.title}'

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья блога'
        verbose_name_plural = 'Статьи блога'
        ordering = ['-create_at', '-update_at', '-views', '-title', '-published']


def toggle_publish(request, pk):
    post_item = get_object_or_404(BlogPost, pk=pk)
    if post_item.published:
        post_item.published = False
    else:
        post_item.published = True
    post_item.save()

    return redirect(reverse('blog:blogpost_list'))
