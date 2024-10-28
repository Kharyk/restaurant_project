from django.contrib import admin
from project.models import Admin, Dish, Table, DishPrice, TablePrice

admin.site.register(Admin)
admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(DishPrice)
admin.site.register(TablePrice)


# Register your models here.
