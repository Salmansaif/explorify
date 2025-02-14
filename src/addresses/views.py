from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
# CRUD
from addresses.models import Address
from billing.models import BillingProfile
from .forms import AddressForm

def checkout_address_create_view(request):
	form = AddressForm(request.POST or None)
	context = {
		"form": form
	}
	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None
	if form.is_valid():
		print(request.POST)
		instance = form.save(commit=False)

		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

		if billing_profile is not None:
			instance.billing_profile = billing_profile
			instance.save()
			request.session["shipping_address_id"] = instance.id
		else:
			print("Error: Not saved!")
			redirect("cart:checkout")

		if is_safe_url(redirect_path, request.get_host()):
			return redirect(redirect_path)

	return redirect("cart:checkout")


def checkout_address_reuse_view(request):
	if request.user.is_authenticated():
		context = {}
		next_ = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_path = next_ or next_post or None
		
		if request.method == "POST":
			print(request.POST)
			shipping_address = request.POST.get('shipping_address', None)
			billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
			if shipping_address is not None:
				qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
				if qs.exists():
					request.session["shipping_address_id"] = shipping_address
				if is_safe_url(redirect_path, request.get_host()):
					return redirect(redirect_path)
	return redirect("cart:checkout")