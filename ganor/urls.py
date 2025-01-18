from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Accounts.urls')),
    path('api/vehicles/', include('Vehicles.urls')),
    path('api/product/', include('Product.urls')),
    path('api/deliveryboy/', include('Delivery_boy.urls')),
    path('api/route/', include('Route.urls')),
    path('api/customer/', include('Customer.urls')),
    path('api/trip/', include('Trip.urls')),
    path('api/bill/', include('Billing.urls')),

]
