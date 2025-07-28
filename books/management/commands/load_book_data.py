from django.core.management.base import BaseCommand
import csv
import pprint
class Command(BaseCommand):
    help = 'Loads book data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
    
        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader, start=1):
                print(f"\n📘 Row {idx}")
                pprint.pprint(row)  # Clean print to inspect
