from django import forms
from .models import Item, Category

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
    
class SellItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'currency', 'delivery_price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'off'}),
            'description': forms.Textarea(attrs={'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super(SellItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['required'] = False