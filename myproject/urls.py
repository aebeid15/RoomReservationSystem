"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views  # Ensure your views module is imported


urlpatterns = [
    path('', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_view, name='admin_dashboard'),
    path('user_page/', views.user_loc_view, name='user_page'),
    path('manage_bookings/', views.manage_bookings, name='user_manage_bookings'),  # Added Manage Bookings
    path('view_history/', views.user_view_history, name='user_view_history'),  # Added View Booking History
    path('user_account/', views.user_account, name='user_account'),
    path('reserve_rooms/', views.user_reserve_rooms, name='user_reserve_rooms'),
    path('manage_rooms/', views.admin_manage_rooms, name='admin_manage_rooms'),
    path('add_room/', views.add_room, name='add_room'),
    path('remove_room/', views.remove_room, name='remove_room'),
    path('update_room/', views.update_room, name='update_room'),
    path('manage_users/', views.admin_manage_users, name='admin_manage_users'),
    path('rooms/', views.view_rooms, name='view_rooms'),
    path('update_booking/', views.update_booking, name='update_booking'), #added new path
    
    #path("reserve_rooms/", views.user_reserve_rooms, name="user_reserve_rooms"),
    #path("manage_bookings/", views.user_manage_bookings, name="user_manage_bookings"),
    #path("view_history/", views.user_view_history, name="user_view_history"),
 
]
