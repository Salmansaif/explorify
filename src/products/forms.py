from django import forms

from .models import Product, Variation


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
			"title",
			"description",
			"price",
			"categories",
			"default",
		]

