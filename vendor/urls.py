from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    # path('registerUser/', views.registerUser, name='registerUser'),
    path('', AccountViews.vendorDashboard, name='vendor'), 
    path('profile/', views.vprofile, name='vprofile'),
]
