from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'stock', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 w-full focus:ring-indigo-500 focus:border-indigo-500'}),
            'price': forms.NumberInput(attrs={'class': 'border border-gray-300 p-2 w-full focus:ring-indigo-500 focus:border-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'border border-gray-300 p-2 w-full focus:ring-indigo-500 focus:border-indigo-500'}),
            'stock': forms.NumberInput(attrs={'class': 'border border-gray-300 p-2 w-full focus:ring-indigo-500 focus:border-indigo-500'}),
            'category': forms.TextInput(attrs={'class': 'border border-gray-300 p-2 w-full focus:ring-indigo-500 focus:border-indigo-500'}),
            'image': forms.ClearableFileInput(attrs={'class': 'border border-gray-300 p-2 w-full focus:ring-indigo-500 focus:border-indigo-500'}),
        }
