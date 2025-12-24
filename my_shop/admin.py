from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage, Order, UserProfile

# 🔹 Ховаємо стандартну категорію "Групи"
admin.site.unregister(Group)


# ================================
#     USER ADMIN
# ================================

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = []  # 🔥 ІНЛАЙН UserProfile ВИМКНЕНО

    fieldsets = (
        ('Основна інформація', {
            'fields': ('username', 'first_name', 'last_name', 'email'),
        }),
    )

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
#      CATEGORY ADMIN
# ================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag')
    search_fields = ('name',)

    def image_tag(self, obj):
        if obj.photo:
            url = obj.photo.url.replace('upload/', 'upload/w_100,f_auto,q_auto/')
            return mark_safe(f'<img src="{url}" />')
        return ""
    image_tag.short_description = 'Фото'


# ================================
#      PRODUCT ADMIN
# ================================

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 2
    verbose_name = "Фото товару"
    verbose_name_plural = "Фотографії товару"
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            url = obj.image.url.replace('upload/', 'upload/w_150,f_auto,q_auto/')
            return mark_safe(f'<img src="{url}" />')
        return ""
    image_tag.short_description = "Прев’ю"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'price', 'article', 'category', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'article')

    def image_preview(self, obj):
        first_image = obj.images.first()
        if first_image:
            url = first_image.image.url.replace('upload/', 'upload/w_100,f_auto,q_auto/')
            return mark_safe(f'<img src="{url}" />')
        return ""
    image_preview.short_description = "Фото"


# ================================
#      ORDER ADMIN
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
            image = p.images.first()
            if image:
                url = image.image.url.replace('upload/', 'upload/w_50,f_auto,q_auto/')
                html += f'<img src="{url}" style="margin-right:5px;" />'
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
