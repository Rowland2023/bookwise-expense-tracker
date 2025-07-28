import csv
import os
from django.core.management.base import BaseCommand
from books.models import Author, Book  # Adjust if your models are elsewhere

class Command(BaseCommand):
    help = "Import books and authors from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        # 🔍 Check if file exists
        if not os.path.isfile(csv_path):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_path}"))
            return

        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=1):
                title = row.get('title')
                author_name = row.get('author')

                if not title or not author_name:
                    self.stderr.write(
                        self.style.WARNING(f"Skipping row {row_num}: Missing title or author")
                    )
                    continue

                # 🔄 Create author if not found
                author, created = Author.objects.get_or_create(name=author_name)

                # 🆗 Create book
                book = Book(title=title, author=author)
                book.save()

                self.stdout.write(self.style.SUCCESS(f"Imported '{title}' by {author.name}"))

        self.stdout.write(self.style.SUCCESS("✅ Import completed successfully."))
