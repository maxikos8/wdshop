from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Category ,  Order, OrderItem


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('title', 'category', 'price', 'available', 'is_bestseller')
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} 

class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "customer_phone", "delivery_method", "status", "created_at")
    search_fields = ("customer_name", "customer_phone")
    list_filter = ("status", "delivery_method")

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
