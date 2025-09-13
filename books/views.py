# 📦 Imports
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from calendar import month_name
from datetime import datetime
from django.utils import timezone
from .forms import TicketForm, ExpenseForm
from .models import Expense, Ticket
from .serializers import TicketSerializer
from django.contrib import messages

import csv

# --------------------------------------------------
# 🔧 Utility Functions
# --------------------------------------------------

def sort_tickets(tickets):
    required_keys = {'created_at', 'id'}
    for ticket in tickets:
        if not required_keys.issubset(ticket):
            raise ValueError("Each ticket must contain 'created_at' and 'id'")
    return [x['id'] for x in sorted(tickets, key=lambda x: (x['created_at'], x['id']))]

def _filter_expenses(request):
    selected_month = request.GET.get('month', '').strip().title()
    selected_category = request.GET.get('category', '').strip().title()
    selected_year = request.GET.get('year', '').strip()

    qs = Expense.objects.all()

    try:
        if selected_month:
            month_number = datetime.strptime(selected_month, '%B').month
            qs = qs.filter(date__month=month_number)
    except ValueError:
        selected_month = ''

    if selected_category:
        qs = qs.filter(category__iexact=selected_category)

    if selected_year.isdigit():
        qs = qs.filter(date__year=int(selected_year))

    return qs, selected_month, selected_category, selected_year

def _get_monthly_expenses(qs):
    return qs.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('month', 'year').annotate(total=Sum('amount')).order_by('year', 'month')

def _get_monthly_ticket_counts():
    ticket_data = Ticket.objects.annotate(
        month=ExtractMonth('created_at'),
        year=ExtractYear('created_at')
    ).values('month', 'year').annotate(count=Count('id'))

    return {
        (entry['month'], entry['year']): entry['count']
        for entry in ticket_data
        if entry['month'] and entry['year']
    }

def _build_chart_data(expenses, ticket_map):
    labels, totals, ticket_counts = [], [], []
    for entry in expenses:
        month, year, total = entry['month'], entry['year'], entry['total']
        if month and year:
            label = f"{month_name[month][:3]} {year}"
            labels.append(label)
            totals.append(float(total))
            ticket_counts.append(ticket_map.get((month, year), 0))
    return labels, totals, ticket_counts

def _get_dropdown_options():
    months = sorted(set(
        month_name[m] for m in Expense.objects.annotate(month=ExtractMonth('date'))
        .values_list('month', flat=True).distinct() if m
    ))

    categories = sorted(set(
        c.strip().title() for c in Expense.objects.values_list('category', flat=True).distinct() if c
    ))

    years = sorted(set(
        Expense.objects.annotate(year=ExtractYear('date'))
        .values_list('year', flat=True).distinct()
    ))

    return months, categories, years

# --------------------------------------------------
# 📊 Reporting Views
# --------------------------------------------------

def report_view(request):
    expenses_qs, selected_month, selected_category, selected_year = _filter_expenses(request)
    expenses = _get_monthly_expenses(expenses_qs)
    ticket_map = _get_monthly_ticket_counts()
    labels, totals, ticket_counts = _build_chart_data(expenses, ticket_map)

    report_data = list(zip(labels, totals, ticket_counts))
    no_data = not report_data

    if no_data:
        report_data = [("No data", 0.0, 0)]
        labels, totals, ticket_counts = zip(*report_data)

    months, categories, years = _get_dropdown_options()

    return render(request, 'books/report.html', {
        'labels': labels,
        'totals': totals,
        'ticket_counts': ticket_counts,
        'report_data': report_data,
        'months': months,
        'categories': categories,
        'years': years,
        'selected_month': selected_month,
        'selected_category': selected_category,
        'selected_year': selected_year,
        'no_data': no_data,
    })

def export_report_csv(request):
    expenses_qs, selected_month, selected_category, selected_year = _filter_expenses(request)
    expenses = _get_monthly_expenses(expenses_qs)
    ticket_map = _get_monthly_ticket_counts()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expense_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Month', 'Total Expenses', 'Ticket Count'])

    for entry in expenses:
        month, year, total = entry['month'], entry['year'], entry['total']
        label = f"{month_name[month][:3]} {year}"
        ticket_count = ticket_map.get((month, year), 0)
        writer.writerow([label, float(total), ticket_count])

    return response

# --------------------------------------------------
# 🎫 Ticket Views
# --------------------------------------------------

@api_view(['POST'])
def ticket_sort_view(request):
    if not isinstance(request.data, list):
        return Response({'error': 'Expected a list of tickets.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TicketSerializer(data=request.data, many=True)
    if serializer.is_valid():
        sorted_ids = sort_tickets(serializer.validated_data)
        return Response({'sorted_ticket_ids': sorted_ids}, status=status.HTTP_200_OK)

    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@login_required
def ticket_dashboard_view(request):
    form = TicketForm()
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "🎫 Ticket submitted successfully!")
            return redirect('ticket-dashboard')

    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')[:10]

    return render(request, 'books/ticket_dashboard.html', {
        'form': form,
        'tickets': tickets
    })

# --------------------------------------------------
# 🏠 Homepage View
# --------------------------------------------------

def homepage_view(request):
    return render(request, 'books/homepage.html')

# --------------------------------------------------
# 👤 User Authentication Views
# --------------------------------------------------

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '🎉 Account created successfully! Welcome aboard.')
            return redirect('dashboard')
        else:
            messages.error(request, '⚠️ Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard_view(request):
    hour = datetime.now().hour
    greeting = (
        "Good morning" if hour < 12 else
        "Good afternoon" if hour < 18 else
        "Good evening"
    )

    form = ExpenseForm()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            # 🔧 Create a ticket automatically
            Ticket.objects.create(
                user=request.user,
                subject=f"Expense: {expense.name}",
                description=f"Amount: {expense.amount}, Category: {expense.category}",
                status="open",
                created_at=timezone.now()
            )

            messages.success(request, "✅ Expense and ticket added successfully!")
            return redirect('dashboard')

    expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]

    return render(request, 'books/dashboard.html', {
        'greeting': greeting,
        'form': form,
        'expenses': expenses,
        'user': request.user,
    })
