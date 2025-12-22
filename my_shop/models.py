from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from cloudinary.models import CloudinaryField


# =========================
# USER PROFILE
# =========================

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile',
        verbose_name="Користувач"
    )
    phone_number = models.CharField("Номер телефону", max_length=15, blank=True)
    address = models.CharField("Адреса", max_length=255, blank=True)

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"

    def __str__(self):
        return self.user.username


# =========================
# CATEGORY
# =========================

class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=100)
    photo = CloudinaryField(
        "Фото категорії",
        folder="categories",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


# =========================
# PRODUCT
# =========================

class Product(models.Model):
    name = models.CharField("Назва товару", max_length=100)
    description = models.TextField("Опис товару")
    price = models.DecimalField("Ціна", max_digits=10, decimal_places=2)
    article = models.CharField("Артикул", max_length=50, default='')
    category = models.ForeignKey(
        Category,
        verbose_name="Категорія",
        related_name='products',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name


# =========================
# PRODUCT IMAGES (MULTIPLE)
# =========================

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        related_name='images',
        on_delete=models.CASCADE
    )
    image = CloudinaryField(
        "Зображення товару",
        folder="products"
    )

    class Meta:
        verbose_name = "Зображення товару"
        verbose_name_plural = "Зображення товарів"


# =========================
# CART
# =========================

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Користувач",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField("Дата створення", default=timezone.now)

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        verbose_name="Кошик",
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Товар",
        related_name='cart_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField("Кількість", default=1)

    class Meta:
        verbose_name = "Товар у кошику"
        verbose_name_plural = "Товари у кошику"


# =========================
# ORDER
# =========================

class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Користувач",
        on_delete=models.CASCADE
    )
    first_name = models.CharField("Ім’я", max_length=100)
    last_name = models.CharField("Прізвище", max_length=100)
    shipping_address = models.CharField("Адреса доставки", max_length=255)
    additional_phone_number = models.CharField(
        "Додатковий телефон",
        max_length=15,
        blank=True
    )
    created_at = models.DateTimeField("Дата створення", default=timezone.now)
    products = models.ManyToManyField(
        Product,
        verbose_name="Товари",
        related_name='orders'
    )

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f"Замовлення користувача {self.user.username} від {self.created_at:%d.%m.%Y}"

    def get_user_phone_number(self):
        return (
            self.user.userprofile.phone_number
            if hasattr(self.user, 'userprofile')
            else ""
        )
