from django.urls import path
from .views import*
urlpatterns = [
    path('create', VehicleCreateView.as_view(), name='vehicle-create'),
    path('edit/<int:pk>', VehicleUpdateView.as_view(), name='edit-update'),
    path('list', VehicleListView.as_view(), name='vehicle-list'),
    path('delete/<int:pk>', VehicleDeleteView.as_view(), name='delete-vehicle'),
    
]

