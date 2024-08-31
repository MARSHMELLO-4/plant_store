from django.contrib import admin
from .models import Plant, Category

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'image')
    fields = ('name', 'price', 'stock', 'description', 'category', 'image')
    # Ensure 'image' is included

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
