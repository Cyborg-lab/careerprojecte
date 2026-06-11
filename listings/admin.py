from django.contrib import admin
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1  

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "price", "created_at")
    list_filter = ("created_at", "brand", "category")
    readonly_fields = ("created_at", "updated_at")  
    prepopulated_fields = {"slug": ("brand", "model", "year")}  
    inlines = [ListingImageInline]

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("listing", "image")