# books/views.py
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear # Import these functions
from .models import Expense
from datetime import datetime
from django.shortcuts import render


def report_view(request):
    # Group expenses by month (and year, for uniqueness if data spans multiple years)
    # Use ExtractMonth to get the month number from the 'date' field
    # It's good practice to also extract the year to differentiate Jan 2024 from Jan 2025
    
    # Option 1: Group by Month Number (e.g., 1 for Jan, 2 for Feb)
    # monthly_data = Expense.objects.values('date__month').annotate(total=Sum('amount')).order_by('date__month')

    # Option 2: Group by Month and Year (more robust for multi-year data)
    # This creates a unique grouping key for each month-year combination
    monthly_data = Expense.objects.annotate(
        month_num=ExtractMonth('date'),
        year_num=ExtractYear('date')
    ).values('month_num', 'year_num').annotate(
        total=Sum('amount')
    ).order_by('year_num', 'month_num')

    # Prepare data for Chart.js
    labels = []
    totals = []

    for entry in monthly_data:
        # Format the label nicely, e.g., "Jan 2024"
        # You might need a mapping for month numbers to names if you prefer names
        month_name = datetime(1, entry['month_num'], 1).strftime('%b') # Converts month number to abbreviated name
        labels.append(f"{month_name} {entry['year_num']}")
        totals.append(float(entry['total'])) # Ensure total is a float for JSON/JS

    return render(request, 'books/report.html', {
        'labels': labels,
        'totals': totals,
    })