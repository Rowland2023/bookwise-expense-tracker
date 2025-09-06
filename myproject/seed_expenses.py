import os
import django
import random
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject")
django.setup()

from expenses.models import Expense  # Adjust to match your app/model name

# Sample categories
categories = ["Food", "Transport", "Utilities", "Entertainment", "Health", "Misc"]

# Generate random expenses
def create_expenses(n=50):
    for _ in range(n):
        Expense.objects.create(
            title=random.choice(["Lunch", "Uber", "Electricity Bill", "Movie", "Pharmacy", "Coffee"]),
            amount=round(random.uniform(5, 100), 2),
            category=random.choice(categories),
            date=datetime.now() - timedelta(days=random.randint(0, 365)),
            notes="Seeded data"
        )
    print(f"✅ {n} expenses created.")

if __name__ == "__main__":
    create_expenses()
