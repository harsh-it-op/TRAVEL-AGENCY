"""
URL Routing for Tourly – Travel Agency Management and Booking System.
Includes standard MVT page routes and JSON AJAX API endpoints.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Core Customer & Auth MVT Views
    path('', views.home_view, name='home'),
    path('destinations/', views.destinations_view, name='destinations'),
    path('destinations/<int:dest_id>/', views.destination_detail_view, name='destination_detail'),
    path('packages/', views.packages_view, name='packages'),
    path('packages/<int:pkg_id>/', views.package_detail_view, name='package_details'),
    path('booking/<int:pkg_id>/', views.booking_view, name='booking'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/cancel/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
    path('contact/', views.contact_view, name='contact'),

    # Custom Bootstrap Administrator Dashboard & CRUD Routes
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-dashboard/destination/save/', views.admin_save_destination, name='admin_save_destination'),
    path('admin-dashboard/destination/delete/<int:dest_id>/', views.admin_delete_destination, name='admin_delete_destination'),
    path('admin-dashboard/package/save/', views.admin_save_package, name='admin_save_package'),
    path('admin-dashboard/package/delete/<int:pkg_id>/', views.admin_delete_package, name='admin_delete_package'),
    path('admin-dashboard/booking/status/<int:booking_id>/', views.admin_update_booking_status, name='admin_update_booking_status'),

    # jQuery AJAX & AngularJS JSON Exchange Endpoints
    path('api/destinations/search/', views.api_search_destinations, name='api_search_destinations'),
    path('api/packages/filter/', views.api_filter_packages, name='api_filter_packages'),
    path('api/packages/<int:pkg_id>/', views.api_package_detail, name='api_package_detail'),
    path('api/contact/submit/', views.api_submit_contact, name='api_submit_contact'),
    path('api/bookings/<int:booking_id>/', views.api_booking_info, name='api_booking_info'),
    path('api/admin/booking-status/', views.api_admin_update_booking, name='api_admin_update_booking'),
]
