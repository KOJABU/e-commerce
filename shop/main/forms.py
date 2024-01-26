from django import forms
from .models import Category , Producer, Brand , Products

PRODUCT_CATEGORY = list()
for i in range(Category.objects.all().count()):
    PRODUCT_CATEGORY.append((i+1, Category.objects.all()[i].name))
print(PRODUCT_CATEGORY)

PRODUCT_BRAND = list() 
for i in range(Brand.objects.all().count()):
    PRODUCT_BRAND.append((i+1, Brand.objects.all()[i].name))
print(PRODUCT_BRAND)

PRODUCT_PRODUCER = list()
for i in range(Producer.objects.all().count()):
    PRODUCT_PRODUCER.append((i+1, Producer.objects.all()[i].name))
print(PRODUCT_PRODUCER)

# PRODUCT_NAME = list()
# for i in (Products.objects.all()):
#     print(i)
#     PRODUCT_NAME.append(i)
# print('AAAAAAA',PRODUCT_NAME)






class AddProductForm2(forms.Form):
    name = forms.CharField(max_length=60)
    price = forms.IntegerField()
    photo = forms.ImageField(required=False)
    pre_description = forms.CharField()
    description = forms.CharField()
    category = forms.TypedChoiceField(choices=PRODUCT_CATEGORY, coerce=str)
    brand = forms.TypedChoiceField(choices=PRODUCT_BRAND,coerce=str)
    producer = forms.TypedChoiceField(choices=PRODUCT_PRODUCER,coerce=str)
    
    
class ChangeProductForm(forms.Form):
    name = forms.CharField(max_length=60)
    price = forms.IntegerField()
    photo = forms.ImageField(required=False, )
    pre_description = forms.CharField()
    description = forms.CharField()
    category = forms.TypedChoiceField(choices=PRODUCT_CATEGORY, coerce=str)
    brand = forms.TypedChoiceField(choices=PRODUCT_BRAND,coerce=str)
    producer = forms.TypedChoiceField(choices=PRODUCT_PRODUCER,coerce=str)


    

