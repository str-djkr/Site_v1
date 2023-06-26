
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, CartItem, Color, Material, GalleryImage
from django.contrib import admin


admin.site.register(CustomUser, UserAdmin)
admin.site.register(GalleryImage)


admin.site.register(Material)
admin.site.register(Color)
admin.site.register(Product)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'color', 'material', 'Success']


admin.site.register(CartItem, CartItemAdmin)
