# books/admin.py
from django.contrib import admin
from .models import Expense, Book, Author, Category, Publisher

admin.site.register(Expense) # Add this line
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Publisher)