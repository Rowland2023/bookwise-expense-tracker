from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 💡 Utility function to sanitize ID inputs
def clean_id(value):
    return None if value in ['Unknown', '', None] else int(value)

# 💸 Safe Expense creation method
def safe_create_expense(data):
    expense = Expense.objects.create(
        user_id=clean_id(data.get('user_id')),
        book_id=clean_id(data.get('book_id')),
        expense_type_id=clean_id(data.get('expense_type_id')),
        amount=data['amount'],
        date=data.get('date', timezone.now())
    )
    return expense

# 📚 Author Model
class Author(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the author")
    bio = models.TextField(blank=True, help_text="Short biography")
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ['name']
        db_table = "books_author"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Author: {self.name}>"


# 📂 Category Model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
        db_table = "books_category"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Category: {self.name}>"


# 🏢 Publisher Model
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"
        ordering = ['name']
        db_table = "books_publisher"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Publisher: {self.name}>"


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
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['-published_date']
        db_table = "books_book"

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<Book: {self.title}>"


# 💸 Expense Type Model
class ExpenseType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Expense Type"
        verbose_name_plural = "Expense Types"
        db_table = "books_expensetype"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<ExpenseType: {self.name}>"


# 💸 Expense Model
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['-date']
        db_table = "books_expense"

    def __str__(self):
        book_title = self.book.title if self.book else "Unlinked"
        type_name = self.expense_type.name if self.expense_type else "Unspecified"
        username = self.user.username if self.user else "Anonymous"
        return f"{type_name} – ₦{self.amount} for {book_title} by {username}"

    def __repr__(self):
        return f"<Expense: ₦{self.amount} on {self.date}>"


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

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ['-created_at']
        db_table = "books_ticket"

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"{self.subject} ({self.status}) by {username}"

    def __repr__(self):
        return f"<Ticket: {self.subject} – {self.status}>"
