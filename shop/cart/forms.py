from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(0,11)]


class AddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int, initial=1
    )

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput())
    
class CartNewProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=[(1,'1')],
        coerce=int, initial=1, required=False, 
        widget=forms.HiddenInput
    )

    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput())