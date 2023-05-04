from django.contrib import admin

from api.models import Category

from api.models import Product, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'category')


@admin.register(Like)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user')
