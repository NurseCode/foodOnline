from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    # path('registerUser/', views.registerUser, name='registerUser'),
    path('', AccountViews.vendorDashboard, name='vendor'), 
    path('profile/', views.vprofile, name='vprofile'),
    path('menu-builder/', views.menu_builder, name='menu_builder'),
    path('menu-builder/category/<int:pk>/', views.items_by_category, name='items_by_category'),
    
    # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # Product Item CRUD
    path('menu-builder/productItem/add/', views.add_ProductItem, name='add_ProductItem'),
    path('menu-builder/edit_product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('menu-builder/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
]

