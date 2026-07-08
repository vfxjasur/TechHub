from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from .models import Brand, Category, ContactMessage, Order, OrderItem, Product, Review


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity')
    verbose_name = _('Товар заказа')
    verbose_name_plural = _('Товары заказа')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)
    ordering = ('order', 'name')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'old_price', 'is_popular', 'in_stock')
    list_filter = ('category', 'brand', 'is_popular', 'in_stock')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)
    list_editable = ('price', 'old_price', 'is_popular', 'in_stock')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'review_date', 'is_active')
    list_filter = ('is_active', 'rating')
    list_display_links = ('author_name',)
    list_editable = ('is_active',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)
    readonly_fields = ('name', 'phone', 'email', 'message', 'created_at')
    list_display_links = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'phone', 'total', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]
    list_display_links = ('pk', 'name')
    list_editable = ('status',)
