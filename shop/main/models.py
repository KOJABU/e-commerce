from django.db import models

# Create your models here.
class Customers(models.Model):
    firs_name = models.CharField(verbose_name='First name of customer', max_length=50)
    last_name = models.CharField(verbose_name='Last name of customer',max_length=50)
    phone = models.CharField(verbose_name='Phone number of product',max_length=20)
    email = models.EmailField(verbose_name='Email of customer')

    def __str__(self):
        return self.firs_name ,self.last_name

class Products(models.Model):
    name = models.CharField(verbose_name='Name of product', max_length=60)
    price = models.IntegerField(verbose_name='Price')
    photo = models.ImageField(verbose_name='Image of product', upload_to='photo/%Y/%m/%d/', default='/photo/2023/12/26/empty.png')
    pre_description = models.CharField(verbose_name='Pre description of product', max_length=90)
    description =  models.TextField(verbose_name="Description of product")
    category  = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category', null=True)
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT,verbose_name='Brand', null=True)
    producer = models.ForeignKey('Producer', on_delete=models.PROTECT,verbose_name='Producer',null=True)

    def __str__(self):
        return self.name 

class Category(models.Model):
    name = models.CharField(verbose_name='Name of category', max_length=60)
    
    def __str__(self):
        return self.name 
    
class Brand(models.Model):
    name = models.CharField(verbose_name = 'Brand of product', max_length=60)
    
    def __str__(self) :
        return self.name


class Producer(models.Model):
    name = models.CharField(verbose_name = 'Producer of product', max_length=60)
    
    def __str__(self) :
        return self.name


