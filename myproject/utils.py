# myproject/utils.py

def sort_tickets(tickets):
    required_keys = {'priority', 'timestamp', 'id'}
    for ticket in tickets:
        if not required_keys.issubset(ticket):
            raise ValueError("Each ticket must contain 'priority', 'timestamp', and 'id'")
    return [x['id'] for x in sorted(tickets, key=lambda x: (x['priority'], x['timestamp'], x['id']))]
