from django.db import models
import datetime
from django.contrib.auth.models import User, auth

# Create your models here.
class category(models.Model):
    def __str__(self):
        return self.name
    
    @staticmethod 
    def get_all_category():
        return category.objects.all()

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)



class item(models.Model):
    def __str__(self):
        return self.name
    
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    desc= models.CharField(max_length=500, null=True, blank=True)
    price= models.IntegerField()
    category = models.ForeignKey(category, on_delete=models.CASCADE, default=1 )
    item_image= models.ImageField(default='default.jpg', upload_to='item_images/')


    @staticmethod
    def get_items_by_id(ids):
        return item.objects.filter(id__in = ids)
    
    @staticmethod
    def get_all_items():
        return item.objects.all()

    @staticmethod
    def get_all_items_by_category_id(category_id):
        if category_id:
            return item.objects.filter(category=category_id)
        else:
            return item.get_all_items()

class Customer(models.Model):
    
    def __str__(self):
        return self.first_name
    

    id = models.AutoField(primary_key=True)
    first_name= models.CharField(max_length=100)            
    last_name= models.CharField(max_length=100)
    phone= models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=500)


    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.get(email = email)
        except:
            return False
        

    def isExists(self):
        if Customer.objects.filter(email = self.email):
            return True

        return False



class Order(models.Model):

    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1, null=True)
    price = models.IntegerField()
    address = models.CharField(max_length=500, null=True)
    phone = models.CharField(max_length=10, null=True)
    date = models.DateTimeField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)
    

   
    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order\
            .objects\
            .filter(customer = customer_id)\
            .order_by('-date')    