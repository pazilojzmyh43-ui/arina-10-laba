from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib import admin
from django.contrib.auth.models import User   # Импорт модели пользователя


class Blog(models.Model):
    """Модель статей блога психологического центра «Пси-Эксперт» (Лекция 9)"""
    
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок статьи"
    )
    
    description = models.TextField(
        verbose_name="Краткое содержание"
    )
    
    content = models.TextField(
        verbose_name="Полное содержание"
    )

    # Новое поле для загрузки изображения
    image = models.FileField(
        upload_to='blog_images/',           # Папка внутри media
        default='temp.jpg',                 # Изображение по умолчанию
        verbose_name="Изображение статьи"
    )
    
    posted = models.DateTimeField(
        default=datetime.now,           # текущая дата и время по умолчанию
        db_index=True,                  # индекс для ускорения поиска по дате
        verbose_name="Опубликована"
    )
    
    author = models.ForeignKey(
        User, 
        null=True,           # Разрешаем NULL в базе (для старых статей)
        blank=True,          # Разрешаем оставлять поле пустым в формах
        on_delete=models.SET_NULL,   # Если автора удалят — поле станет NULL
        verbose_name="Автор статьи"
    )

    def __str__(self):
        """Метод строкового представления объекта"""
        return self.title
    
    def get_absolute_url(self):
        """Возвращает URL для конкретной статьи (удобно для ссылок)"""
        return reverse('blog_detail', kwargs={'pk': self.pk}) 
    
    class Meta:
        verbose_name = "Статья блога"           # Название в единственном числе в админке
        verbose_name_plural = "Статьи блога"    # Название во множественном числе
        ordering = ['-posted']                  # Сортировка по дате публикации (новые сверху)

admin.site.register(Blog)   # Регистрируем модель в админке (лекция 8 + 9)

class Comment(models.Model):
    """Модель комментариев к статьям блога"""
    
    post = models.ForeignKey(
        Blog, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name="Статья"
    )
    
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Автор комментария"
    )
    
    text = models.TextField(verbose_name="Текст комментария")
    
    date = models.DateTimeField(
        default=datetime.now, 
        verbose_name="Дата комментария"
    )
    
    def __str__(self):
        return f"{self.author} - {self.post.title[:30]}..."
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date']   # Новые комментарии сверху


class Category(models.Model):
    """Категория информационного каталога услуг центра (лабораторная 10)"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название категории"
    )
    description = models.TextField(
        verbose_name="Описание"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория каталога"
        verbose_name_plural = "Категории каталога"
        ordering = ['name']


class CatalogItem(models.Model):
    """Элемент каталога — услуга психологического центра"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название"
    )
    short_description = models.TextField(
        verbose_name="Краткое описание"
    )
    full_description = models.TextField(
        verbose_name="Полное описание"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    image = models.FileField(
        upload_to='catalog_images/',
        verbose_name="Ссылка на картинку"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )

    def __str__(self):
        return self.name

    @property
    def price_display(self):
        """Цена для страницы каталога. Ноль — бесплатная услуга."""
        if self.price == 0:
            return "Бесплатно"
        amount = int(self.price) if self.price == self.price.to_integral() else self.price
        text = f"{amount:,}".replace(",", " ")
        return f"{text} ₽"

    class Meta:
        verbose_name = "Элемент каталога"
        verbose_name_plural = "Элементы каталога"
        ordering = ['name']


admin.site.register(Category)
admin.site.register(CatalogItem)