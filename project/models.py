from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, F
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from datetime import date, timedelta
from decimal import Decimal



class CartOfPrivileges(models.Model):
    
    DISCOUNT = [
        ('10', '10'),
        ('15', '15'),
        ('30', '30'),
    ]
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    discount = models.CharField(max_length=2, choices=DISCOUNT, default='10')  # Default to 10% discount
    startdate = models.DateField(auto_now=True)
    enddate = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def create_end_date(self):
        self.enddate = date.today() + timedelta(days=365)
        self.save()
        return self.enddate
    
    
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_data = f"Client: {self.id_client.username}\nDiscount: {self.discount}%\nStart Date: {self.startdate}"
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        filename = f'qr_code_{self.id_client.username}.png'
        
        self.qr_code.save(filename, File(buffer), save=False)
        
    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.generate_qr_code()
        if not self.enddate:
            self.create_end_date()
        super().save(*args, **kwargs)

class Allergies(models.Model):
    
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class LanguageOfCommunication(models.Model):
    
    language = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.language
    
    
    
class ExtraInfoUser(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    allergies = models.ManyToManyField(Allergies)
    language_of_communication = models.ManyToManyField(LanguageOfCommunication)
    discount = models.ManyToManyField(CartOfPrivileges, blank=True)
    foto = models.ImageField(upload_to='foto_user/', blank=True)


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
    allergies = models.ManyToManyField(Allergies)
    image = models.ImageField(upload_to='dish_img/', blank=True, null=True)
    

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
    image = models.ImageField(upload_to="table_img/", blank=True, null=True)
    

class DishPrice(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=False)
    

class TablePrice(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=False)
    text = models.TextField(blank=True)
    

class Comment(models.Model):
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField( upload_to= "comment_img/", blank = True, null = True)
    
    
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
        ("Paid", "Paid"),
        ("Want to pay", "Want to pay"),
        ("Current", "Current")
    ]
    
    id_client = models.ForeignKey(User, on_delete=models.CASCADE)
    id_table = models.ForeignKey('Table', on_delete=models.CASCADE)  
    date = models.DateTimeField(auto_now_add=True, editable=True)  
    status = models.CharField(max_length=20, choices=STATUS, default="Current")

    def calculate_price(self):
        if not self.id_client or not self.id_table:
            return 0.00 
        
        total = 0 
        btw = 21
        
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
            
        discount = CartOfPrivileges.objects.filter(id_client=self.id_client).first()
        if discount:
            discount_percentage = int(discount.discount)
            total *= Decimal(1 - (discount_percentage / 100))
    
        if btw:
            print("btw")
            total = total * Decimal(1 + btw / 100)
    
            
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
    
    
  