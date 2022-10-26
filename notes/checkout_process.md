1. Cart -> Checkout View ?

	Login/Register or Enter an Email (as Guest)
	Shipping Address
	Billing Info
		Billing Address
		Credit Card / Payment
		
2. Billing App/Component
	Billing Profile
		User or Email (Guest Email)
		generate payment processor token (Stripe or Braintree)

3. Orders / Invoices Component
	Connecting the Billing Profile
	Shipping / Billing Address
	Cart
	Status -- Shipped? Cancelled?

4. Backup Fixtures python manage.py dumpdata products --format json --indent 4 > products/fixtures/products.json
	deleted migrations folder & db than makemigrations & migrate
	-Restore Fixtures:
	first saved the json file to utf-8, than
	python manage.py migrate --run-syncdb
	python manage.py loaddata products/fixtures/products.json