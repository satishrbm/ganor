from django.urls import path
from .views import *


urlpatterns = [
    
    path('customers/<int:route_id>/<str:from_date>/<str:to_date>/', route_customer, name='route_customer_date_range'),
    path('generate_bill_api/', generate_bill, name='generate_bill_api'),
    path('bill_list/', BillsListView.as_view(), name='bills-list'),
    path('customer_bills/<int:customer_id>/', customer_bill_list, name='bill-list'),


]
