from django.contrib import admin

# Register your models here.


from product_app.models import CategoryModel, ProductModel

@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug')

    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'price', 'stock', 'is_active')

    list_filter = ('category', 'color', 'sizes_available')

    search_fields = ('name', 'description')

    prepopulated_fields = {'slug': ('name',)}

