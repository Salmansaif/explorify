from django.conf.urls import url

from .views import (ProductListView, 
					ProductDetailView,
					product_create_view,
					)

urlpatterns = [
	url(r'^$', ProductListView.as_view(), name='list'),
	url(r'^create/$', product_create_view),
	url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),
]