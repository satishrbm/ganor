from django.urls import path
from .views import*
from .import views


urlpatterns = [
    path('ordernumber', get_order_number, name='get_order_number'),
    path('create', CustomerCreateView.as_view(), name='customer-create'),
    path('list', CustomerListView.as_view(), name='customer-closelist'),
    path('closecustomer', create_close_customer.as_view(), name='closecustomer'),
    path('closelist', CloseCustomerListView.as_view(), name='customer-list'),
    path('delete/<int:pk>', CustomerDeleteView.as_view(), name='customer-delete'),
    path('edit/<int:pk>', CustomerUpdateView.as_view(), name='customer-edit'),
    path('routelist', RouteListView.as_view(), name='routelist'),
    path('sequences', SequenceAPIView.as_view(), name='sequences_api'),
    path('bottleupdate', BottleAPIView.as_view(), name='bottleupdate'),
    path('updatebottle', views.update_total_bottle, name='updatebottle'),
    path('landmarks/create', views.LandmarkCreateView.as_view(), name='landmark-create'),
    path('landmarks', views.LandmarkListView.as_view(), name='landmark-list'),
    path('close_customer', views.CloseCustomerkListView.as_view(), name='close_customer'),
    path('landmarks/delete/<int:pk>', delete_landmark , name='landmark-delete'),
    path('customer_reactive/<int:pk>/', CustomerRestartView.as_view(), name='customer_reactive'),

    #========== Mobile App API ===========

    path('customerlogin', views.App_login_customer, name='customerlogin'),

    # path('user_delevery/', UserDeleveryListCreateView.as_view(), name='user_delevery-list-create'),
    path('extramilk/', UserDeleveryCreateView.as_view(), name='user_delevery-create'),

]
