from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField(default = 0)
    image_url = models.CharField(max_length=2000)
    category = models.CharField(max_length=100)
    pub_date = models.DateField()
    desc = models.TextField()
    rating = models.IntegerField(default=0)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=250,unique=True)
    address = models.CharField(max_length=500)
    phone = models.IntegerField(default=0)
    Age = models.IntegerField(default=0)
    sex = models.CharField(max_length=1)

    def __str__(self):
        return self.name

class Cart(models.Model):
    cart_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.cart_id

class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + "("+self.customer.name+")"

class Tracker(models.Model):
    tracker_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    def __str__(self):
        return str(self.tracker_id)

