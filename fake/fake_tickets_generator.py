import hmac
import requests
import json
import random
from datetime import timedelta, datetime


def make_header(body, secret):
    unix_timestamp = str(datetime.timestamp(datetime.now())).split('.')[0]
    body_to_sign = f'{unix_timestamp}.{body}'.encode()
    digest = hmac.new(secret.encode(), body_to_sign, "sha256").hexdigest()
    # Set the headers for the POST request
    headers = {'Petzi-Signature': f't={unix_timestamp},v1={digest}', 'Petzi-Version': '2',
               'Content-Type': 'application/json', 'User-Agent': 'PETZI webhook'}
    return headers


def make_post_request(url, data, secret):
    try:
        # Make the POST request
        response = requests.post(url, data=data.encode('utf-8'), headers=make_header(data, secret))

        if response.status_code == 200:
            print(f"Request successful. Response: {response.text}")
        else:
            print(f"Request failed with status code {response.status_code}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def random_date(start_date, end_date):
    """Generate a random datetime between two dates."""
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))


def generate_dummy_tickets(num_tickets=100):
    """Generate a list of dummy ticket data."""
    events = ["Concert", "Festival", "Theater Show", "Comedy Night", "Sports Game"]
    locations = [
        {"name": "Case a Chocs", "street": "Quai Philipe Godet 20", "city": "Neuchatel", "postcode": "2000"},
        {"name": "Hall 7", "street": "Avenue des Champs", "city": "Geneva", "postcode": "1200"},
        {"name": "Arena", "street": "Rue de la Musique 3", "city": "Lausanne", "postcode": "1000"},
    ]
    ticket_types = ["online_presale", "at_door", "vip", "early_bird"]
    categories = ["Standard", "VIP", "Prelocation", "Group"]
    promoters = ["Case à Chocs", "Live Nation", "EventBrite", "Swiss Events"]

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)

    tickets = []

    for _ in range(num_tickets):
        event = random.choice(events)
        location = random.choice(locations)
        ticket_number = f"{random.randint(1000, 9999)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{random.randint(1000, 9999)}"
        generated_at = random_date(start_date, end_date).isoformat()

        ticket_data = {
            "event": "ticket_created",
            "details": {
                "ticket": {
                    "number": ticket_number,
                    "type": random.choice(ticket_types),
                    "title": event,
                    "category": random.choice(categories),
                    "eventId": random.randint(1000, 99999),
                    "event": event,
                    "cancellationReason": "",
                    "generatedAt": generated_at,
                    "sessions": [
                        {
                            "name": event,
                            "date": generated_at.split("T")[0],
                            "time": f"{random.randint(10, 23)}:00:00",
                            "doors": f"{random.randint(8, 22)}:00:00",
                            "location": location
                        }
                    ],
                    "promoter": random.choice(promoters),
                    "price": {
                        "amount": str(random.randint(10, 200)) + ".00",
                        "currency": "CHF"
                    }
                },
                "buyer": {
                    "role": "customer",
                    "firstName": random.choice(["Jane", "John", "Alice", "Bob", "Charlie", "David"]),
                    "lastName": random.choice(["Doe", "Smith", "Johnson", "Williams", "Brown", "Davis"]),
                    "postcode": str(random.randint(1000, 9999))
                }
            }
        }
        tickets.append(ticket_data)

    return tickets


# Generate 200 dummy tickets and save to a file
dummy_tickets = generate_dummy_tickets(200)

for dummy_ticket in dummy_tickets:
    url = "http://localhost:5000/insert"
    secret = "coucou"
    data = json.dumps(dummy_ticket, indent=4)
    # Make the POST request
    make_post_request(url, data, secret)

