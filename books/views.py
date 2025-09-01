from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Expense, Ticket
from .serializers import TicketSerializer
from myproject.utils import sort_tickets


from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime
from calendar import month_name

from .models import Expense, Ticket


def report_view(request):
    # 🔹 Normalize and sanitize inputs
    selected_month = request.GET.get('month', '').strip().title()
    selected_category = request.GET.get('category', '').strip().title()
    selected_year = request.GET.get('year', '').strip()

    # 🔹 Prepare dropdown options
    month_numbers = Expense.objects.annotate(
        month=ExtractMonth('date')
    ).values_list('month', flat=True).distinct()
    months = sorted(set(month_name[m] for m in month_numbers if m))

    raw_categories = Expense.objects.values_list('category', flat=True).distinct()
    categories = sorted(set(c.strip().title() for c in raw_categories if c))

    year_numbers = Expense.objects.annotate(
        year=ExtractYear('date')
    ).values_list('year', flat=True).distinct()
    years = sorted(set(year_numbers))

    # 🔹 Filter expenses
    expenses_qs = Expense.objects.all()

    try:
        if selected_month:
            month_number = datetime.strptime(selected_month, '%B').month
            expenses_qs = expenses_qs.filter(date__month=month_number)
    except ValueError:
        selected_month = ''

    if selected_category:
        expenses_qs = expenses_qs.filter(category__iexact=selected_category)

    if selected_year.isdigit():
        expenses_qs = expenses_qs.filter(date__year=int(selected_year))

    # 🔹 Aggregate expenses
    expenses = expenses_qs.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('month', 'year').annotate(total=Sum('amount')).order_by('year', 'month')

    # 🔹 Aggregate tickets
    ticket_data = Ticket.objects.annotate(
        month=ExtractMonth('timestamp'),
        year=ExtractYear('timestamp')
    ).values('month', 'year').annotate(count=Count('id'))

    ticket_map = {
        (entry['month'], entry['year']): entry['count']
        for entry in ticket_data
        if entry['month'] and entry['year']
    }

    # 🔹 Build chart and table data
    labels, totals, ticket_counts = [], [], []
    for entry in expenses:
        month, year, total = entry['month'], entry['year'], entry['total']
        if month and year:
            label = f"{month_name[month][:3]} {year}"
            labels.append(label)
            totals.append(float(total))
            ticket_counts.append(ticket_map.get((month, year), 0))

    report_data = list(zip(labels, totals, ticket_counts))
    no_data = len(report_data) == 0

    # 🔹 Fallback if no data
    if no_data:
        labels = ["No data"]
        totals = [0.0]
        ticket_counts = [0]
        report_data = [("No data", 0.0, 0)]

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


def _get_monthly_expenses(queryset):
    return queryset.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('month', 'year').annotate(
        total=Sum('amount')
    ).order_by('year', 'month')


def _get_monthly_ticket_counts():
    ticket_data = Ticket.objects.annotate(
        month=ExtractMonth('timestamp'),
        year=ExtractYear('timestamp')
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
            label = f"{datetime(1900, month, 1).strftime('%b')} {year}"
            labels.append(label)
            totals.append(float(total))
            ticket_counts.append(ticket_map.get((month, year), 0))

    return labels, totals, ticket_counts


@api_view(['POST'])
def ticket_sort_view(request):
    if not isinstance(request.data, list):
        return Response({'error': 'Expected a list of tickets.'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = TicketSerializer(data=request.data, many=True)
    if serializer.is_valid():
        sorted_ids = sort_tickets(serializer.validated_data)
        return Response({'sorted_ticket_ids': sorted_ids}, status=status.HTTP_200_OK)

    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def ticket_dashboard_view(request):
    sort_order = request.GET.get('sort', 'asc')
    order_by = 'priority' if sort_order == 'asc' else '-priority'

    tickets = Ticket.objects.select_related('expense').order_by(order_by, 'timestamp')

    return render(request, 'books/ticket_dashboard.html', {
        'tickets': tickets,
        'sort_order': sort_order,
    })


import csv
from django.http import HttpResponse

def export_report_csv(request):
    selected_month = request.GET.get('month', '').strip().title()
    selected_category = request.GET.get('category', '').strip().title()
    selected_year = request.GET.get('year', '').strip()

    expenses_qs = Expense.objects.all()

    try:
        if selected_month:
            month_number = datetime.strptime(selected_month, '%B').month
            expenses_qs = expenses_qs.filter(date__month=month_number)
    except ValueError:
        selected_month = ''

    if selected_category:
        expenses_qs = expenses_qs.filter(category__iexact=selected_category)

    if selected_year.isdigit():
        expenses_qs = expenses_qs.filter(date__year=int(selected_year))

    expenses = expenses_qs.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('month', 'year').annotate(total=Sum('amount')).order_by('year', 'month')

    ticket_data = Ticket.objects.annotate(
        month=ExtractMonth('timestamp'),
        year=ExtractYear('timestamp')
    ).values('month', 'year').annotate(count=Count('id'))

    ticket_map = {
        (entry['month'], entry['year']): entry['count']
        for entry in ticket_data
        if entry['month'] and entry['year']
    }

    # Create CSV response
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


def homepage_view(request):
    return render(request, 'books/homepage.html')
