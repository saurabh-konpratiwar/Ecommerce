from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    pub_date = models.DateField()
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
       return self.product_name




class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    item_JSON = models.CharField(max_length=5000)
    name = models.CharField(max_length=111)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111,default='')
    amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."

class Advertise(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(max_length=1000)
    launchDate = models.DateField()
    img = models.ImageField(upload_to="shop/images", default="")


    def __str__(self):
        return self.name




class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500,default="")


    def __str__(self):
        return self.name



