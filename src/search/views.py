from django.shortcuts import render
from django.views.generic import ListView, DetailView

from products.models import Product

class SearchProductView(ListView):
	template_name = "search/view.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['query'] = self.request.GET.get('q')
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		print(request.GET)
		query = request.GET.get('q')
		if query is not None:
			return Product.objects.search(query)
		return Product.objects.featured()