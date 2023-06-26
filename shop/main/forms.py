from django import forms
from django.db import models


class LoginForm(forms.Form):
    username = forms.CharField(label='Ім\'я користувача')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class ProductFilterForm(forms.Form):
    category = forms.CharField(max_length=100, required=False)
    min_price = forms.DecimalField(decimal_places=2, required=False)
    max_price = forms.DecimalField(decimal_places=2, required=False)
    #^^фільтри


from .models import GalleryImage


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ('image',)


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)  # Поле для введення кількості товару
    color = forms.CharField(max_length=50)  # Поле для вибору кольору
    material = forms.CharField(max_length=50)  # Поле для вибору матеріалу