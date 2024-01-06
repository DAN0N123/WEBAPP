from django.contrib import admin
from store.models import Item

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('symbol', 'total_price')

admin.site.register(Item, ItemAdmin)
