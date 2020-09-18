from django.db import models

# Create your models here.

class  Product(models.Model):
    image = models.ImageField(upload_to='products/', blank=True)
    name = models.CharField(max_length=300)
   
    product_quantity=models.IntegerField()
    product_category= models.CharField(max_length=300)
    product_type= models.CharField(max_length=300)
    attribute = models.TextField(max_length=1000, verbose_name='attribute')
    price = models.FloatField()
    discount_price=models.FloatField()
    

    def __str__(self):
        return self.name