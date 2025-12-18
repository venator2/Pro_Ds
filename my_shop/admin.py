from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage, Order, UserProfile

# 🔹 Ховаємо стандартну категорію "Групи"
admin.site.unregister(Group)


# ================================
#     USER ADMIN (без інлайну!)
# ================================

# Прибираємо стандартне відображення User
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = []  # 🔥 ІНЛАЙН UserProfile ПОВНІСТЮ ВИМКНЕНО

    # Показуємо тільки потрібні поля
    fieldsets = (
        ('Основна інформація', {
            'fields': ('username', 'first_name', 'last_name', 'email'),
        }),
    )

    # Ховаємо зайве
    exclude = (
        'password',
        'is_staff',
        'is_superuser',
        'is_active',
        'last_login',
        'date_joined',
        'groups',
        'user_permissions',
    )

    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')


# ================================
#          CATEGORY ADMIN
# ================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    verbose_name = "Категорія"
    verbose_name_plural = "Категорії"


# ================================
#          PRODUCT ADMIN
# ================================

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 2
    verbose_name = "Фото товару"
    verbose_name_plural = "Фотографії товару"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'article', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'article')
    verbose_name = "Товар"
    verbose_name_plural = "Товари"


# ================================
#           ORDER ADMIN
# ================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Інформація про товари', {'fields': ['product_information']}),
        ('Інформація про користувача', {'fields': ['user_information']}),
        ('Деталі замовлення', {
            'fields': [
                'shipping_address',
                'get_user_phone_number',
                'additional_phone_number',
                'created_at'
            ]
        }),
    ]

    readonly_fields = [
        'product_information',
        'user_information',
        'shipping_address',
        'get_user_phone_number',
        'additional_phone_number',
        'created_at'
    ]

    list_display = (
        '__str__',
        'shipping_address',
        'get_user_phone_number',
        'additional_phone_number',
        'created_at'
    )

    def product_information(self, obj):
        products = obj.products.all()
        if not products:
            return "Немає товарів"

        html = ""
        for p in products:
            html += f"<b>Назва:</b> {p.name} — <b>Артикул:</b> {p.article}<br>"

        return mark_safe(html)

    product_information.short_description = "Інформація про товари"

    def user_information(self, obj):
        profile = getattr(obj.user, "userprofile", None)

        phone = profile.phone_number if profile else "—"
        email = obj.user.email or "—"

        return mark_safe(
            f"<b>Ім'я:</b> {obj.first_name}<br>"
            f"<b>Прізвище:</b> {obj.last_name}<br>"
            f"<b>Телефон:</b> {phone}<br>"
            f"<b>Email:</b> {email}"
        )

    user_information.short_description = "Інформація про користувача"


# ================================
#      CUSTOM ADMIN HEADERS
# ================================

admin.site.site_header = "Адміністративна панель магазину"
admin.site.site_title = "Керування магазином"
admin.site.index_title = "Головна сторінка адміністратора"

