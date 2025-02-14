from django.shortcuts import render, redirect
from django.http import JsonResponse

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from addresses.models import Address
from addresses.forms import AddressForm
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart

def cart_detail_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{
			"id": x.id,
			"url": x.get_absolute_url(),
			"name": x.title, 
			"price": x.price
			}
			for x in cart_obj.products.all()]
	cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
	return JsonResponse(cart_data)


def cart_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)

	return render(request, "carts/cart.html", {"cart": cart_obj})


# for updating cart, if changed
def cart_update(request):
	product_id = request.POST.get('product_id')
	if product_id is not None:
		try:
			product_obj = Product.objects.get(id=product_id)
		except Product.DoesNotExist:
			print("Show message to user, product is gone?")
			redirect("cart:home")
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		if product_obj in cart_obj.products.all():
			cart_obj.products.remove(product_obj)
			added = False
		else:
			cart_obj.products.add(product_obj)
			added = True
		request.session['cart_items_count'] = cart_obj.products.count()
		if request.is_ajax():
			print("Ajax request")
			json_data = {
				"added": added,
				"removed": not added,
				"cartItemCount": cart_obj.products.count(),
			}
			return JsonResponse(json_data, status=200) # HttpResponse
			# return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
	return redirect("cart:home")


def checkout_home(request):
	cart_obj, cart_created = Cart.objects.new_or_get(request)
	order_obj = None
	if cart_created or cart_obj.products.count() == 0:
		return redirect("cart:home")

	login_form = LoginForm()
	guest_form = GuestForm()
	address_form = AddressForm()
	shipping_address_id = request.session.get("shipping_address_id", None)

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
	address_qs = None
	if billing_profile is not None:
		if request.user.is_authenticated():
			address_qs = Address.objects.filter(billing_profile=billing_profile)
		print(address_qs)
		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			order_obj.save()
			del request.session["shipping_address_id"]

	if request.method == "POST":
		"some check that order is done"
		is_done = order_obj.check_done()
		if is_done:
			order_obj.mark_paid()
			request.session["cart_items_count"] = 0
			del request.session["cart_id"]
			return redirect("cart:success")


	context = {
		"object": order_obj,
		"billing_profile": billing_profile,
		"login_form": login_form,
		"guest_form": guest_form,
		"address_form": address_form,
		"address_qs": address_qs,
	}
	return render(request, "carts/checkout.html", context)


def checkout_done_view(request):
	return render(request, "carts/checkout-done.html", {})