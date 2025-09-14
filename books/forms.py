# books/forms.py
from django import forms
from .models import Expense
from .models import Ticket  # Make sure Ticket model exists

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'description']  # Adjust based on your model fields

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['book', 'expense_type', 'amount']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'expense_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
        }
