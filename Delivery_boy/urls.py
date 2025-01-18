from django.urls import path
from .views import *


urlpatterns = [
    path('create', DeliveryboyCreateView.as_view(), name='deleveryboy-create'),
    path('list', DeliveryboyListView.as_view(), name='deleveryboy-list'),
    path('edit/<int:pk>', DeliveryboyUpdateView.as_view(), name='deleveryboy-edit'),
    path('delete/<int:pk>', DeliveryboyDeleteView.as_view(), name='deleveryboy-delete'),
    path('ordernumber', get_order_number, name='get_order_number'),
]
