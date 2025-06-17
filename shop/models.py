from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Генерируем slug автоматически, если не задан
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)  # Главное фото
    desc = models.TextField(blank=True)
    is_bestseller = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    seo_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="SEO Title")
    seo_description = models.TextField(blank=True, null=True, verbose_name="SEO Description")
    seo_keywords = models.CharField(max_length=255, blank=True, null=True, verbose_name="SEO Keywords")

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('self', 'Самовывоз'),
        ('cdek', 'СДЭК'),
        ('yandex', 'Яндекс'),
    ]
    name = models.CharField("ФИО", max_length=100)
    phone = models.CharField("Телефон", max_length=30)
    email = models.EmailField("Email", blank=True, null=True)
    delivery = models.CharField("Способ доставки", choices=DELIVERY_CHOICES, max_length=10)
    address = models.CharField("Адрес/ПВЗ", max_length=255, blank=True, null=True)
    comment = models.TextField("Комментарий", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # для “быстрого поиска” — можно добавить order_id/статус

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} — {self.id}"