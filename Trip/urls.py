from django.urls import path
from .views import*

urlpatterns = [
    path('tripnumber', get_order_number, name='get_trip_number'),
    path('create/', TripCreateView.as_view(), name='trip-list-create'),
    path('route/<int:route_id>/', getdata.as_view(), name='delivery-boys-vehicles'),
    path('routelist', RouteListView.as_view(), name='route_list'),
    path('triplist', TripListView.as_view(), name='triplist'),
    path('delete/<int:pk>', TripDeleteView.as_view(), name='trip-delete'),
    path('customers', CusstomerList.as_view(), name='customers'),
    path('customer/routeupdate/', BulkUpdateCustomersRoute.as_view(), name='routeupdate'),

    path('generate_full_month_schedule/<int:customer_id>/',generate_two_months_schedule,name = 'generate_full_month_schedule'),
    
    path('tripprint/<int:trip_id>/', trip_slip.as_view(), name='tripprint'),
    path('tripview/<int:trip_id>/', Trip_View.as_view(), name='tripview'),


# temporary api 

    path('routecustomer/<int:route_id>/', get_route_customers_data.as_view(), name='route_customer'),

    path('customersearch', customersearch.as_view(), name='customersearch'),
    path('updatemilksupply', UpdateSupplyAPIView.as_view(), name='updatemilksupply'),
    path('bulk_bottle_update/', update_today_return_bottle, name='supply-bulk-update'),
]
#calculate_today_bottle