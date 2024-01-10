from django.contrib import admin
from store.models import *
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'display_cart', 'display_favorites')
    ordering = ('email',)
    def display_cart(self, obj):
        return ", ".join([str(item) for item in obj.cart.all()])
    def display_favorites(self, obj):
        return ", ".join([str(item) for item in obj.favorites.all()])
    
    display_cart.short_description = 'Cart'
    display_favorites.short_description = 'Favorites'
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('total_price', 'favorites')
    filter_horizontal = ['category']

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Message)