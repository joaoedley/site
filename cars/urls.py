from django.urls import path
from .views import (
    CarListView, CarDetailView, SearchResultsView,
    add_to_cart, view_cart, remove_from_cart, checkout, update_quantity
)

app_name = 'cars'

urlpatterns = [
    path('', CarListView.as_view(), name='car_list'),
    path('category/<slug:category_slug>/', CarListView.as_view(), name='car_list_by_category'),
    path('<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('add-to-cart/<int:car_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/update/<int:order_id>/', update_quantity, name='update_quantity'),
    path('remove-from-cart/<int:order_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    
]