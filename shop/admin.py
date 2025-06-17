from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Category


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

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
