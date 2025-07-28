from django.contrib import admin
from .models import Book, Author, Category, Publisher

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_date')
    search_fields = ('title',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Publisher)
