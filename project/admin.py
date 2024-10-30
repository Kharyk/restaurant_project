from django.contrib import admin
from project.models import Dish, Table, DishPrice, TablePrice, Order, Check, Comment, Stars

admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(DishPrice)
admin.site.register(TablePrice)
admin.site.register(Order)
admin.site.register(Check)
admin.site.register(Comment)
admin.site.register(Stars)



# Register your models here.
