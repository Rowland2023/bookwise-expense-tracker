from django.contrib import admin
from .models import Author, Category, Publisher, Book, Expense, Ticket

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'publisher', 'published_date')
    list_filter = ('category', 'publisher', 'published_date')
    search_fields = ('title', 'author__name')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'date', 'category', 'book')
    list_filter = ('category', 'date', 'book')
    search_fields = ('name', 'book__title')
    date_hierarchy = 'date'


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'expense', 'priority', 'status', 'submitted_by', 'timestamp')
    list_filter = ('status', 'priority', 'timestamp')
    search_fields = ('expense__name', 'submitted_by__username')
    date_hierarchy = 'timestamp'
