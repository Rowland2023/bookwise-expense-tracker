from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Author, Category, Publisher, Book, Expense, Ticket

# 🔹 Custom User Admin (removes password field when editing)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # editing existing user
            form.base_fields.pop('password', None)
        return form

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# 🔹 Author Admin
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 🔹 Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# 🔹 Publisher Admin
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

# 🔹 Book Admin
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'published_date')  # ✅ Removed 'author' and 'category' if not in model
    list_filter = ('publisher', 'published_date')            # ✅ Removed 'category' if not in model
    search_fields = ('title',)

# 🔹 Expense Admin
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date', 'book')  # ✅ Removed 'category'
    list_filter = ('date', 'book')                     # ✅ Removed 'category'
    search_fields = ('book__title',)
    date_hierarchy = 'date'
# 🔹 Ticket Admin
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    date_hierarchy = 'created_at'
