#
# This script insert dummy data for testing purposes
# You can configure the date range of the ticket
#       start_date = datetime(2025, 2, 1)
#       end_date = datetime(2025, 2, 13)
# You can choose the number of tickets to create
#       num_tickets = 3000
# Don't forget to set the correct petzi secret shared with the server
#       secret = "coucou"
# After setting this variables, just launch the script.
#
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
            print(f"[+] Request successful. Response: {response.text}")
        else:
            print(f"Request failed with status code {response.status_code}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def random_date(start_date, end_date):
    """Generate a random datetime between two dates."""
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))


def generate_dummy_tickets(num_tickets=100):
    """Generate a list of dummy ticket data."""
    events = [
        "WALTER ASTRAL + FOREST LAW", "SUBLIMINAL X BODY DANCE SYNTH MUSIC", "A.K.A IDIOTS FIRST SHOW",
        "RUE OBERKAMPF + POTOCHKINE", "BSA SOUNDSYSTEM: INVASION TEKNO",
        "CIGARETTE CITY ALLSTARZ", "A TABLE",  "10 ANS DU LABEL ASTROPOLIS", "VALENTINO VIVACE + LOLA BASTARD"
    ]
    # Create a mapping from event names to event IDs
    event_id_mapping = {event: random.randint(1000, 99999) for event in events}

    locations = [
        {"name": "Case a Chocs", "street": "Quai Philipe Godet 20", "city": "Neuchatel", "postcode": "2000"},
        {"name": "Hall 7", "street": "Avenue des Champs", "city": "Neuchatel", "postcode": "1200"},
        {"name": "Arena", "street": "Rue de la Musique 3", "city": "Lausanne", "postcode": "1000"},
    ]
    ticket_types = ["online_presale", "at_door", "vip", "early_bird"]
    categories = ["Standard", "VIP", "Prelocation", "Group"]
    promoters = ["Case à Chocs", "Live Nation", "EventBrite", "Swiss Events"]

    start_date = datetime(2025, 2, 1)
    end_date = datetime(2025, 2, 13)

    tickets = []

    # Define peak periods (e.g., specific days or hours with higher ticket sales)
    peak_periods = [
        datetime(2025, 2, 5, 18, 0),  # Peak on February 5th at 6 PM
        datetime(2025, 2, 10, 20, 0),  # Peak on February 10th at 8 PM
    ]

    for _ in range(num_tickets):
        event = random.choice(events)
        location = random.choice(locations)
        ticket_number = f"{random.randint(1000, 9999)}{random.choice('ABCDEFGHJKLMNPQRSTUVWXYZ')}{random.randint(1000, 9999)}"

        # Simulate peaks of ticket sales
        if random.random() < 0.2:  # 20% chance of generating a ticket during a peak period
            peak_time = random.choice(peak_periods)
            generated_at = peak_time + timedelta(minutes=random.randint(-60, 60))  # Add some randomness
        else:
            generated_at = random_date(start_date, end_date)  # Normal ticket generation

        ticket_data = {
            "event": "ticket_created",
            "details": {
                "ticket": {
                    "number": ticket_number,
                    "type": random.choice(ticket_types),
                    "title": event,
                    "category": random.choice(categories),
                    "eventId": event_id_mapping[event],
                    "event": event,
                    "cancellationReason": "",
                    "generatedAt": generated_at.isoformat(),
                    "sessions": [
                        {
                            "name": event,
                            "date": generated_at.strftime("%Y-%m-%d"),
                            "time": generated_at.strftime("%H:%M:%S"),
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


num_tickets = 3000
dummy_tickets = generate_dummy_tickets(num_tickets)

counter = 0
for dummy_ticket in dummy_tickets:
    counter += 1
    print("[+] TICKET " + str(counter) + " / " + str(num_tickets))
    url = "http://localhost:5000/insert"
    secret = "coucou"
    data = json.dumps(dummy_ticket, indent=4)
    # Make the POST request
    make_post_request(url, data, secret)
