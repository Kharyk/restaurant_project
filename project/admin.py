from django.contrib import admin
from project.models import Dish, Table, DishPrice, TablePrice, Order, Check, Comment, Stars



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'number', 'date')
    search_fields = ('id_client__username',)
    
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     obj.total_price = obj.calculate_price()
    #     obj.save(update_fields=['total_price'])

admin.site.register(Order, OrderAdmin)
admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(DishPrice)
admin.site.register(TablePrice)
admin.site.register(Check)
admin.site.register(Comment)
admin.site.register(Stars)



# Register your models here.
