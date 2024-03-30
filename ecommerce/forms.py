from django import forms

from ecommerce.models import PAYMENT_METHOD_CHOICES

class EditCartItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

class CreateOrderForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
