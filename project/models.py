from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F

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
        ("Beverages", "beverages"),
        ("Soups", "soups"),
        ("Salads", "salads")
    ]
    
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    gram = models.CharField(max_length=255)
    sort_daytime = models.CharField(max_length=15, choices=SORTDT, blank=True, null=True)
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
    
    name = models.CharField(max_length=255)
    number_of_people = models.IntegerField()
    zone = models.CharField(max_length=10, choices=ZONE)
    sort = models.CharField(max_length=20, choices=SORT)
    

class DishPrice(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=False)
    

class TablePrice(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=False)
    

class Comment(models.Model):
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True) 
    
    
class Stars(models.Model):
    
    STARS = [
        ("One", "one"),        
        ("Two", "two"),
        ("Three", "three"),
        ("Four", "four"),
        ("Five", "five")
    ]
    
    id_dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    stars = models.CharField(max_length=5, choices=STARS)  
    date = models.DateTimeField(auto_now_add=True) 



class Order(models.Model):
    STATUS = [
        ("Reserved", "done"),
        ("In the basket", "not_done")
    ]
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_dishes = models.ManyToManyField(Dish, blank=True) 
    id_table = models.ManyToManyField(Table, blank=True)  
    number = models.IntegerField()  
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    status = models.CharField(max_length=20, choices=STATUS, default="not_done")

    def calculate_price(self):
        total = 0
        for dish in self.id_dishes.all():
            latest_price = DishPrice.objects.filter(dish=dish, date__lte=self.date).order_by('-date').first()
            if latest_price:
                total += latest_price.price * self.number
        return total

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        self.total_price = self.calculate_price()
        super(Order, self).save(update_fields=['total_price'])

class Check(models.Model):
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_table = models.ForeignKey(Table, on_delete=models.CASCADE)  
    id_order = models.ManyToManyField(Order, blank=True)  
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    
    def calculate_total_price(self):
        if not self.id_client or not self.id_table:
            return 0.00  
        
        orders_in_basket = Order.objects.filter(id_client=self.id_client, status="not_done")
        
        total = sum(order.total_price for order in orders_in_basket) 
        
        latest_table_price = TablePrice.objects.filter(table=self.id_table, date__lte=self.date).order_by('-date').first()
        if latest_table_price:
            total += latest_table_price.price 
        
        return total

    def get_dish_names(self):
        if not self.id_client:
            return []  
        
        dish_names = set()  
        orders_in_basket = Order.objects.filter(id_client=self.id_client, status="not_done")
        
        for order in orders_in_basket:
            for dish in order.id_dishes.all():
                dish_names.add(dish.name)  
        
        return list(dish_names) 

    def mark_orders_as_done(self):
        if not self.id_client:
            return
        
        orders_in_basket = Order.objects.filter(id_client=self.id_client, status="not_done")
        
        for order in orders_in_basket:
            order.status = "Reserved" 
            order.save()  

    def save(self, *args, **kwargs):
        super(Check, self).save(*args, **kwargs)  
        
        self.total_price = self.calculate_total_price()
        super(Check, self).save(update_fields=['total_price'])
        
        self.mark_orders_as_done()