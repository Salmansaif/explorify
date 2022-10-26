import os

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify

from explorify.utils import unique_slug_generator


class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(featured=True, active=True)

	def search(self, query):
		lookups = (Q(title__icontains=query) | 
					Q(description__icontains=query) | 
					Q(price__icontains=query)|
					Q(tag__title__icontains=query)) # related tags
		return self.filter(lookups).distinct()


class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def featured(self): #Product.objects.featured()
		return self.get_queryset().featured()

	def get_related(self, instance):
		products_one = self.get_queryset().filter(categories__in=instance.categories.all())
		products_two = self.get_queryset().filter(default=instance.default)
		qs = (products_one | products_two).exclude(id=instance.id).distinct()
		return qs

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id) #Product.objects == self.get_queryset()
		if qs.count() == 1:
			return qs.first()
		return None

	def search(self, query):
		return self.get_queryset().active().search(query)


class Product(models.Model):
	title = models.CharField(max_length=150)
	slug = models.SlugField(blank=True, unique=True)
	description = models.TextField()
	# summary = models.TextField()
	price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	categories = models.ManyToManyField('Category', blank=True)
	default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)

	objects = ProductManager()

	def get_absolute_url(self):
		# return "{slug}/".format(slug=self.slug)
		return reverse("products:detail", kwargs={"slug": self.slug})

	def get_image_url(self):
		img = self.productimage_set.first()
		if img:
			return img.image.url
		else: img #None

	def __str__(self):
		return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)


class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sell_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True) # refers none == unlimited amount


	def __str__(self):
		return self.title

	def get_price(self):
		if self.sell_price is not None:
			return self.sell_price

		else:
			return self.price

	def get_absolute_url(self):
		return self.product.get_absolute_url()

# whenever the PRODUCT model data is posted for save, it'll callback to this receiver
def product_post_saved_receiver(sender, instance, created, *args, **kwargs): # receiver function
	product = instance
	variations = product.variation_set.all()
	# variations = Variation.objects.filter(product=product) # same as above
	if variations.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.price = product.price
		new_var.save()
	# print(sender)
	# print(instance)
	# print(created)

post_save.connect(product_post_saved_receiver, sender=Product) # connecting receiver to signal


def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

# ISSUE TO RESOLVE: image isn't deleting when object get destroyed
def image_upload_to(instance, filename):
	title = instance.product.title
	slug = slugify(title)
	name, ext = get_filename_ext(filename)
	new_filename = "{}-{}{}".format(slug, instance.id, ext) # also add random numbers
	return "products/{}/{}".format(slug, new_filename)


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to)

	def __str__(self):
		return self.product.title


class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug})