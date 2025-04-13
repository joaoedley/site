
from django.contrib import admin
from .models import Category, Car, Order

admin.site.register(Category)
admin.site.register(Car)
admin.site.register(Order)

class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'available')
    list_filter = ('available', 'transmission')
    search_fields = ('make', 'model')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'car_count')
    prepopulated_fields = {'slug': ('name',)}

    def car_count(self, obj):
        return obj.car_set.count()
    car_count.short_description = 'Carros'