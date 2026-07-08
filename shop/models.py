from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Иконка')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Цена')
    old_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name='Старая цена')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name='Бренд')
    image = models.ImageField(upload_to='products/', blank=True, verbose_name='Изображение')
    image_url = models.URLField(blank=True, help_text='Используется когда нет загруженного изображения', verbose_name='URL изображения')
    is_popular = models.BooleanField(default=False, verbose_name='Популярный')
    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-is_popular', '-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or '/static/img/product-placeholder.svg'

    @property
    def has_discount_property(self):
        return self.old_price and self.old_price < self.price


class Review(models.Model):
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    author_initial = models.CharField(max_length=2, verbose_name='Инициалы')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Рейтинг')
    review_date = models.DateField(verbose_name='Дата отзыва')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    order_ref = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ', related_name='reviews')

    class Meta:
        ordering = ['order', '-review_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.author_name


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.name} — {self.created_at:%d.%m.%Y}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('confirmed', 'Подтверждён'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.TextField(blank=True, verbose_name='Адрес')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    total = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name='Сумма')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.pk} — {self.name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='Товар')
    product_name = models.CharField(max_length=200, verbose_name='Название товара')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name='Телефон')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Полное имя')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name='Фото профиля')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.username}'
