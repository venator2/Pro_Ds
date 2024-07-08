from django.contrib import admin
from .models import Category, Product, ProductImage, Order

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'description', 'price', 'article', 'category')

class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Product Information', {
            'fields': ['product_information'],
            'classes': ['wide']
        }),
        ('User Information', {
            'fields': ['user_information'],
            'classes': ['wide']
        }),
        ('Order Details', {
            'fields': ['shipping_address', 'get_user_phone_number', 'additional_phone_number', 'created_at'],
            'classes': ['wide']
        }),
    ]
    readonly_fields = ['product_information', 'user_information', 'shipping_address', 'get_user_phone_number', 'additional_phone_number', 'created_at']

    list_display = ('__str__', 'shipping_address', 'get_user_phone_number', 'additional_phone_number', 'created_at')

    def product_information(self, obj):
        product_info = ""
        for product in obj.products.all():
            product_info += f"Name: {product.name}, Article: {product.article}\n"
        return product_info

    product_information.short_description = "Product Information"

    def user_information(self, obj):
        user_info = f"Name: {obj.user.first_name} {obj.user.last_name}\n"
        return user_info

    user_information.short_description = "User Information"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
