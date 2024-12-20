from django import forms
from .models import Product, Order


class ProductForm(forms.ModelForm):
         
    class Meta:
        model = Product
        fields = ['name','quantity','category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            placeholder = f'Enter {field.label.lower()}' if field.label else 'Enter value'
            field.widget.attrs.update({'class': 'form-control', 'placeholder': placeholder})
class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'order_quantity']
