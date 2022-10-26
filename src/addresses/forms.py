from django import forms

from .models import Address

class AddressForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['address_line_1'].widget.attrs.update({"class": "form-control", "placeholder": "Your Address"})
		self.fields['address_line_1'].label="Address Line 1"
		self.fields['address_line_2'].widget.attrs.update({"class": "form-control", "placeholder": "Your Address"})
		self.fields['address_line_2'].label="Address Line 2 (Optional)"
		self.fields['country'].widget.attrs.update({"class": "form-control"})
		self.fields['province'].widget.attrs.update({"class": "form-control"})
		self.fields['city'].widget.attrs.update({"class": "form-control"})
		self.fields['postal_code'].widget.attrs.update({"class": "form-control", "placeholder": "Enter Postal Code"})

	class Meta:
		model = Address
		fields = [
			# 'billing_profile',
			'address_line_1',
			'address_line_2',
			'city',
			'province',
			'country',
			'postal_code',
		]