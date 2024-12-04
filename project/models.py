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
    image = models.ImageField( upload_to='dish_img/', blank = True, null = True)
    

class Table(models.Model):
    
    ZONE = [
        ("Indoors", "indoors"),        
        ("Outdoors", "outdoors")
    ]
    
    SORT = [
        ("VIP", "vip"),
        ("General", "general"),
        ("Appointment", "appointment")
    ]
    
    name = models.CharField(max_length=255)
    number_of_people = models.IntegerField()
    zone = models.CharField(max_length=10, choices=ZONE)
    sort = models.CharField(max_length=20, choices=SORT)
    image = models.ImageField(upload_to= "table_img/", blank = True, null = True)
    

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
    image = models.ImageField( upload_to= "omment_img/", blank = True, null = True)
    
    
class Stars(models.Model):
    
    STARS = [
        ("One", "one"),        
        ("Two", "two"),
        ("Three", "three"),
        ("Four", "four"),
        ("Five", "five")
    ]
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE, null = True)
    id_dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    stars = models.CharField(max_length=5, choices=STARS)  
    date = models.DateTimeField(auto_now_add=True) 


class Check(models.Model):
    
    STATUS = [
        ("Paid", "paid"),
        ("Want to pay", "wtp"),
        ("In process", "not paid")
    ]
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_table = models.ForeignKey('Table', on_delete=models.CASCADE)  
    date = models.DateTimeField(auto_now_add=True, editable=True)  
    status = models.CharField(max_length=20, choices=STATUS, default="not paid")

    def calculate_price(self):
        if not self.id_client or not self.id_table:
            return 0.00 
        
        total = 0 
        
        all_orders = self.orders.all()
        print(f'All orders related to check ID {self.id}: {[order.id for order in all_orders]}')
         
        
        print(f'Calculating price for check ID: {self.id}.')
        
        for order in all_orders:
            print(f'Processing Order ID: {order.id}, Number: {order.number}')
            
            for dish in order.id_dishes.all():
                print(f'Found Dish: {dish.name} in Order ID: {order.id}')
                latest_price = DishPrice.objects.filter(dish=dish, date__lte=self.date).order_by('-date').first()
                
                if latest_price:
                    dish_total = latest_price.price * order.number
                    total += dish_total
                    
                    print(f'Dish: {dish.name}, Price: {latest_price.price:.2f}, Quantity: {order.number}, Total: {dish_total:.2f}')
                else:
                    print(f'No price found for Dish: {dish.name}')
        
        latest_table_price = TablePrice.objects.filter(table=self.id_table, date__lte=self.date).order_by('-date').first()
        if latest_table_price:
            total += latest_table_price.price 
        
        return total
    
    def get_dish_names(self):
        if not self.id_client:
            return []  
        
        dish_names = set()  
        
        all_orders = self.orders.all()

        for order in all_orders:
            for dish in order.id_dishes.all():
                dish_names.add(dish.name)  
        
        return list(dish_names) 
    
    def get_latest_price(self, date):
        return self.tableprice_set.filter(date__lte=date).order_by('-date').first()


        
            
    def save(self, *args, **kwargs):
        super(Check, self).save(*args, **kwargs)  
        
        
        total_price = self.calculate_price()
        print(f'Total price for the check: {total_price:.2f}') 
        
        dish_names = self.get_dish_names()
        print(f'Dishes in the check: {", ".join(dish_names)}')
        
        for order in self.orders.all():
            print(f'Order ID: {order.id}, Number: {order.number}')
        
        
       

class Order(models.Model):
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_dishes = models.ManyToManyField(Dish, blank=True) 
    id_check = models.ForeignKey(Check, on_delete=models.CASCADE, blank=True, null=True, related_name="orders")
    number = models.IntegerField()  
    date = models.DateTimeField(auto_now_add=True)

    def get_dish_prices(self):
        dish_prices = []
        for dish in self.id_dishes.all():
            # Get the latest price for the dish based on the order date
            latest_price = DishPrice.objects.filter(dish=dish, date__lte=self.date).order_by('-date').first()
            if latest_price:
                dish_prices.append({
                    'dish_name': dish.name,
                    'price': latest_price.price,
                    'quantity': self.number,
                    'total_price': latest_price.price * self.number
                })
        return dish_prices