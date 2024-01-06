from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = []  # Include all fields in the form

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_delivery_price(self):
        delivery_price = self.cleaned_data.get('delivery_price')
        if delivery_price is not None and delivery_price < 0:
            raise forms.ValidationError("Delivery price cannot be negative.")
        return delivery_price