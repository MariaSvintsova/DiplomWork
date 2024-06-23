from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from products.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, toggle_activity, \
    ProductDeleteView

# app_name = MainConfig.name
app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_update'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
]

