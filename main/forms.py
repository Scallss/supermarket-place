from django import forms
from .models import Product
from django.utils.html import strip_tags

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

    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_description(self):
        description = self.cleaned_data["description"]
        return strip_tags(description)
    
    def clean_category(self):
        category = self.cleaned_data["category"]
        return strip_tags(category)