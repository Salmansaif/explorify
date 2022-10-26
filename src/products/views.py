import random

from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from analytics.mixins import ObjectViewedMixin
from .mixins import StaffRequiredMixin
from .models import Product, Category
from .forms import ProductForm
from carts.models import Cart


def product_create_view(request):
	form = ProductForm(request.POST or None)
	if form.is_valid():
		form.save()

	context = {
		'form': form
	}
	return render(request, "products/product_create.html", context)


# class ProductInventoryView(CreateView):
# 	form_class = ProductInventoryForm
# 	template_name = 'products/inventory.html'
# 	success_url = '/products/'


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all().featured()
	template_name = "products/product_detail.html"

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	return Product.objects.featured()

class ProductListView(ListView):
	queryset = Product.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self, *args, **kwargs): #also get_queryset could be used
		request = self.request
		return Product.objects.all()


class ProductDetailView(ObjectViewedMixin, DetailView):
	queryset = Product.objects.all()
	
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		instance = self.get_object()
		context["related"] = sorted(Product.objects.get_related(instance)[:6], key=lambda x: random.random())
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		print("---------------")
		print(cart_obj, new_obj)
		context["cart"] = cart_obj
		return context

	def get_object(self, *args, **kwargs):
		instance = self.get_object()
		ObjectViewedMixin
		# object_viewed_signal.send(instance.__class__, instance=instance, request=request)


class CategoryListView(ListView):
	queryset = Category.objects.all()


class CategoryDetailView(ObjectViewedMixin, DetailView):
	queryset = Category.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = (product_set | default_products).distinct()
		context["products"] = products
		return context

# class ProductDetailView(DetailView):
# 	# queryset = Product.objects.all()
# 	# template_name = "products/product_detail.html"

# 	def get_context_data(self, *args, **kwargs):
# 		context = super().get_context_data(*args, **kwargs)
# 		# print(context)
# 		return context

# 	def get_object(self, *args, **kwargs): #also get_queryset could be used
# 		request = self.request
# 		pk = self.kwargs.get("pk")
# 		instance = Product.objects.get_by_id(pk)
# 		if instance is None:
# 			raise Http404("Product doesn't exist")
# 		return instance