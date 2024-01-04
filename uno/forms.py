from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

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

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
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
    

class PostForm(forms.Form):
    post_text = forms.CharField(max_length=500, label="", widget=forms.Textarea(attrs={'placeholder': 'Your message here'}))
    
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
