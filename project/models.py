from django.db import models

#client, admin
from django.contrib.auth.models import User


class Admin(models.Model):
    first_name = models.CharField(max_length=50)
    famely_name = models.CharField( max_length=50)
    bday = models.DateField()
    start_of_work = models.DateField()
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    medical_book = models.FileField(upload_to= "med_book/", max_length=100)
    

#dish, table
class Dish(models.Model):
    
    SORTDT = [
        ("Breakfast", "breakfast"),
        ("Lunch", "lunch"),
        ("Dinner", "dinner")
    ]
    
    SORT = [
        ("Appetizers", "appetizers"),
        ("Main Courses", "main"),
        ("Side Dishes", "side"),
        ("Desserts", "desserts"),
        ("Beverages", "deverages"),
        ("Soups", "soups"),
        ("Salads", "salads")
    ]
    
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    gram = models.CharField(max_length=255)
    sort_daytime = models.CharField(max_length=15, choices=SORTDT, blank= True, null= True)
    sort = models.CharField(max_length=50, choices=SORT)
    
class Table(models.Model):
    
    ZONE = [
        ("Indoors", "indoors"),        
        ("Outdoors", "outdoors")

    ]
    
    SORT = [
        ("PIV", "piv"),
        ("General", "general"),
        ("Appointment", "appointment")

    ]
    
    name = models.IntegerField()
    number_of_people = models.FloatField()
    zone = models.CharField(max_length=10, choices = ZONE)
    sort = models.CharField(max_length=20, choices = SORT)

    
#prices for dishes and tables
class DishPrice(models.Model):
    dish = models.ManyToManyField("Dish")
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=False)
    
class TablePrice(models.Model):
    table = models.ManyToManyField("Table")
    price = models.FloatField()
    date = models.DateTimeField(("table_date_time"), auto_now_add=False)
    
    
#comment

#order

#check

# extra: discounts









# class Order(models.Model):
# user = models.ForeignKey(User, on_delete=models.CASCADE)
# dish = models.ManyToManyField("Dish", verbose_name=_("dish"))(Dish, on_delete=models.CASCADE)
# number = models.FloatField()
# # class Check(models.Model):
# # user = models.ForeignKey(User, on_delete=models.CASCADE)
# # table = models.ForeignKey("Table", on_delete=models.CASCADE)
# # order = models.ForeignKey("Order", on_delete=models.CASCADE)
# # price = models.FloatField()
# # date = models.DateTimeField(("check_date_time"), auto_now_add=False)
