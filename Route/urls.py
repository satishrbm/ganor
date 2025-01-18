from django.urls import path
from .views import*
from . import views




urlpatterns = [
    path('create', RouteCreateView.as_view(),name="create-route"),
    path('edit/<int:pk>', RouteUpdateView.as_view(), name='route-edit'),
    path('list', RouteListView.as_view(), name='route-list'),
    path('delete/<int:pk>', RouteDeleteView.as_view(), name='route-delete'),
    path('deliveryboy', DeliveryBoyListView.as_view(), name='delivery_boys_list'),
    path('vehicles', VehicleListView.as_view(), name='vehicle_list'),
    path('route/<int:route_id>/', getdata.as_view(), name='route_customers'),
    path('customer/<int:customer_id>/', getCustomerdata.as_view(), name='customers'),
]

