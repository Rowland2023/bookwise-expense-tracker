from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 📚 Author, Category, Publisher Models
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Publishers"

    def __str__(self):
        return self.name


# 📖 Book Model
class Book(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=255, default="", blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, related_name='books')
    published_date = models.DateField(blank=True, null=True)
    distribution_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name_plural = "Books"
        ordering = ['-published_date']

    def __str__(self):
        return self.title


# 💸 Expense Model
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Expenses"
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} ({self.category}) - ₦{self.amount} by {self.user.username}"

# 🎟️ Ticket Model
class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #expense = models.ForeignKey(Expense, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "Tickets"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} ({self.status}) by {self.user.username}"