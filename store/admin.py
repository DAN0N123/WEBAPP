from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from store.models import Item, Category

class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('symbol', 'total_price')
    filter_horizontal = ['category']

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)
