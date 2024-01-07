from django import forms
from .models import Item, Category, CustomUser
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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    def clean(self):
        users = CustomUser.objects.all()
        user_names = [user.username for user in users]
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        confirm_password = cleaned_data.get('confirm_password')
        for field_name, value in cleaned_data.items():
            if not value and self.fields[field_name].required:
                self.add_error(field_name, forms.ValidationError("This field is required"))
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        if username not in user_names:
            raise forms.ValidationError("Such user does not exist")

        return cleaned_data
    
class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        for field_name, value in cleaned_data.items():
            if not value and self.fields[field_name].required:
                self.add_error(field_name, forms.ValidationError("This field is required"))
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data