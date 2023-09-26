from django.urls import path

from .views import CustomAuthToken, StaffListCreateView, StaffDetailUpdateView, ExpenceListView, ExpenceDetailUpdateView, ReturnListView, ReturnDetailUpdateView, ProductDetailUpdateView, ProductListView, SalesView

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('staffs/', StaffListCreateView.as_view(), name='staff_list_view'),
    path('staffs/<id>', StaffDetailUpdateView.as_view(), name='staff_detail_view'),
    path('expence/', ExpenceListView.as_view(), name='expence_list_view'),
    path('expence/<id>/', ExpenceDetailUpdateView.as_view(), name='expence_detail_view'),
    path('return/', ReturnListView.as_view(), name='return_list_view'),
    path('return/<id>/', ReturnDetailUpdateView.as_view(), name='return_detail_view'),
    path('product/', ProductListView.as_view(), name='product_list_view'),
    path('product/<id>/', ProductDetailUpdateView.as_view(), name='product_detail_view'),
    path('sales/', SalesView.as_view(), name='sales_list_view'),
]