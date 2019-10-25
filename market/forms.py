from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'quantity_available', 'category', 'delisted']

    def clean(self):
        pass

    def save(self, commit=True):
        product = super(ProductForm, self).save(commit=False)
        if commit:
            product.save()
            self.save_m2m()
        return product


