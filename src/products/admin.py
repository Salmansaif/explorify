from django.contrib import admin

from .models import Product, Variation, Category, ProductImage

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'slug']
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(Category)
admin.site.register(ProductImage)