
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


# ---------------- TIMESTAMPED ----------------

class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ---------------- CATEGORY ----------------

class Category(Timestamped):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if not self.slug and self.pk is None:
            super().save(*args, **kwargs)

        if not self.slug:
            self.slug = f"{slugify(self.title)}-{self.id}"
            Category.objects.filter(id=self.id).update(slug=self.slug)

    def __str__(self):
        return self.title


# ---------------- PRODUCT ----------------

class Product(Timestamped):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, blank=True)

    short_desc = models.CharField(max_length=240, blank=True)
    description = models.TextField(blank=True)

    # Индивидуальная цена материала за 1 м²
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Цена материала за м² (сом)'
    )

    # Индивидуальная цена нанесения за 1 м²
    application_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Цена нанесения за м² (сом)'
    )

    is_published = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = f"{slugify(self.title)}-{self.id}"
            Product.objects.filter(id=self.id).update(slug=self.slug)
            return

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ---------------- PRODUCT IMAGES ----------------

class ProductImage(Timestamped):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(upload_to='products/')
    alt = models.CharField(max_length=160, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Фото изделия'
        verbose_name_plural = 'Фото изделий'

    def __str__(self):
        return self.product.title


# ---------------- REVIEW ----------------

class Review(Timestamped):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    name = models.CharField(max_length=120)

    rating = models.PositiveSmallIntegerField(
        default=10,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    text = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# ---------------- ORDER ----------------

class Order(Timestamped):
    SERVICE_CHOICES = [
        ('material', 'Только материал'),
        ('both', 'Материал и нанесение'),
        ('application', 'Только нанесение'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    address = models.CharField(max_length=255, blank=True)

    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )

    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_CHOICES,
        default='both'
    )

    # Цены, сохранённые на момент оформления заказа
    material_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    application_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    comment = models.TextField(blank=True)

    status = models.CharField(
        max_length=32,
        default='new'
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.product or 'Без товара'}"
