from django.urls import path
from books.views import dashboard_view
from django.contrib.auth import views as auth_views
from books.views import ticket_dashboard_view
from books.views import (
    homepage_view,
    report_view,
    export_report_csv,
    ticket_dashboard_view,
    ticket_sort_view,
    register,  # 👈 Make sure this view exists in books/views.py
)

urlpatterns = [
    path('', homepage_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('reports/', report_view, name='report'),
    path('reports/export/', export_report_csv, name='export_report_csv'),
    path('tickets/', ticket_dashboard_view, name='ticket-dashboard'),
    path('sort-tickets/', ticket_sort_view, name='sort-tickets'),
    path('accounts/register/', register, name='register'),  # 👈 Add this line
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
