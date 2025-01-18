from django.urls import path
from Product.views import*

urlpatterns = [
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='product-edit'),
    path('list', ProductListView.as_view(), name='product-list'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='product-delete'),
]
