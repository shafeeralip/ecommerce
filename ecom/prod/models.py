from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name


class  Product(models.Model):
    PRODUCTTYPE={
    ("shirt", "shirt"), 
    ("t-shirt", "t-shirt"), 
    ("pant", "pant"), 
    ("jeans", "jeans"), 
    ("sunglass", "sunglass"), 
    ("shoe", "shoe"), 
    }
    PRODUCTCATEGORY={
    ("Apparel", "Apparel"), 
    ("Acessories", "Acessories"), }

    image = models.ImageField(null=True ,blank=True)
    name = models.CharField(max_length=300)
    price = models.FloatField()
   
    product_quantity=models.IntegerField()
    product_category= models.CharField(max_length=300,choices=PRODUCTCATEGORY)
    product_type= models.CharField(max_length=300,choices=PRODUCTTYPE)
    attribute = models.TextField(max_length=1000, verbose_name='attribute')
    
    
    

    def __str__(self):
        return self.name
    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url


class Order(models.Model):

    STATUS={
        ("pending","pending"),
        ("shipped","shipped"),
        ("out for delivery","out for delivery"),
        ("completed","completed")

    }


    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True,blank=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=True)
    transaction_id=models.CharField(max_length=200,null=True)
    approve= models.BooleanField(default=False,null=True,blank=True)
    value=models.CharField(default='pending',max_length=200,null=True )
    



   

    def __str__(self):
        return str(self.id)
    
    # def __iter__(self):
    #     return  [field.value_to_string(self) for field in Order.customer]



    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
 
    @property
    def shipping(self):
        shipping = True
        return shipping




class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True,blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True,blank=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address






