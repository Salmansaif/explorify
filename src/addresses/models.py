from django.db import models

from billing.models import BillingProfile

countries = [
		('pak', 'Pakistan'),
		('uk', 'United Kingdom')
	]

cities = [
	('khi', 'Karachi'),
]

province = [
	('sd', 'Sindh'),
	# ('pj', 'Punjab'),
	# ('bl', 'Balochistan'),
	# ('kpk', 'Khaibar Pakhtoon Khua'),
]

class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile)
	address_line_1 	= models.CharField(max_length=120)
	address_line_2 	= models.CharField(max_length=120, null=True, blank=True)
	city 			= models.CharField(max_length=120, choices=cities, default="Karachi")
	province 		= models.CharField(max_length=120, choices=province, default="Sindh")
	country 		= models.CharField(max_length=120, choices=countries, default="Pakistan")
	postal_code 	= models.CharField(max_length=120)

	def __str__(self):
		return str(self.billing_profile)

	def get_address(self):
		return "{line1}\n{line2}\n{city}\n{province}\n{country}\n{postal}".format(
				line1=self.address_line_1,
				line2=self.address_line_2 or "",
				city=self.city,
				province=self.province,
				country=self.country,
				postal=self.postal_code
			)