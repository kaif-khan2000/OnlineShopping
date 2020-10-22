from django.contrib import admin
from .models import Product,Customer,Cart,Order,Tracker
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Tracker)