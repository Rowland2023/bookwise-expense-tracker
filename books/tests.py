from django.test import TestCase
from django.urls import reverse
from .models import Expense, Ticket
from datetime import date


class BaseTestSetup(TestCase):
    def setUp(self):
        self.expense = Expense.objects.create(
            name="Design",
            amount=2000,
            date=date.today(),
            category="Design"
        )
        self.ticket1 = Ticket.objects.create(
            expense=self.expense,
            priority=2,
            status='pending',
            submitted_by=None
        )
        self.ticket2 = Ticket.objects.create(
            expense=self.expense,
            priority=1,
            status='approved',
            submitted_by=None
        )


class TicketSortTests(BaseTestSetup):
    def test_ticket_sort_api_returns_sorted_ids(self):
        payload = [
            {
                'id': self.ticket1.id,
                'priority': self.ticket1.priority,
                'timestamp': self.ticket1.timestamp.isoformat()
            },
            {
                'id': self.ticket2.id,
                'priority': self.ticket2.priority,
                'timestamp': self.ticket2.timestamp.isoformat()
            }
        ]
        response = self.client.post(
            reverse('sort-tickets'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('sorted_ticket_ids', response.json())


class ReportViewTests(TestCase):
    def setUp(self):
        Expense.objects.create(name="Printing", amount=5000, date=date(2025, 8, 1), category="Production")
        Expense.objects.create(name="Marketing", amount=3000, date=date(2025, 8, 15), category="Promotion")
        expense = Expense.objects.first()
        Ticket.objects.create(expense=expense, priority=1, status='pending', submitted_by=None)

    def test_report_view_returns_correct_chart_data(self):
        response = self.client.get(reverse('report'))
        self.assertEqual(response.status_code, 200)

        context = response.context
        self.assertIn('labels', context)
        self.assertIn('totals', context)
        self.assertIn('ticket_counts', context)

        self.assertEqual(context['labels'], ["Aug 2025"])
        self.assertEqual(context['totals'], [8000.0])
        self.assertEqual(context['ticket_counts'], [1])


class TicketDashboardViewTests(TestCase):
    def setUp(self):
        expense = Expense.objects.create(name="Design", amount=2000, date=date(2025, 9, 1), category="Production")
        Ticket.objects.create(expense=expense, priority=2, status='pending')
        Ticket.objects.create(expense=expense, priority=1, status='resolved')

    def test_dashboard_view_sorts_tickets_ascending(self):
        response = self.client.get(reverse('ticket_dashboard') + '?sort=asc')
        self.assertEqual(response.status_code, 200)

        tickets = response.context['tickets']
        self.assertEqual(len(tickets), 2)
        self.assertLessEqual(tickets[0].priority, tickets[1].priority)
