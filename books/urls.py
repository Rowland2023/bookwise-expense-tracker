from django.urls import path
from .views import export_report_csv
from . import views

urlpatterns = [
    path('', views.homepage_view, name='home'),  # 👈 This is your root URL
    path('reports/', views.report_view, name='report'),
    path('sort-tickets/', views.ticket_sort_view, name='sort-tickets'),
    path('tickets/', views.ticket_dashboard_view, name='ticket-dashboard'),
    path('dashboard/', views.ticket_dashboard_view, name='ticket_dashboard'),
    path('reports/export/', export_report_csv, name='export_report_csv'),
]
