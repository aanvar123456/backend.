from django.contrib import admin
from .models import Staffs, Expences, Products, Returns, Sales

# Register your models here.
admin.site.register(Staffs)
admin.site.register(Expences)
admin.site.register(Products)
admin.site.register(Returns)
admin.site.register(Sales)