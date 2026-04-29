import time
import json
import random
import requests
from datetime import datetime

# Configuration
API_URL = "http://136.110.48.196/collect"  # Updated with LoadBalancer IP
EVENT_TYPES = ["view_item", "add_to_cart", "purchase"]
ITEM_IDS = [f"item_{i}" for i in range(1, 101)]
USER_IDS = [f"user_{i}" for i in range(1, 51)]

def generate_event():
    # 90% clean data, 10% dirty data
    is_dirty = random.random() < 0.10
    
    event = {
        "user_id": random.choice(USER_IDS) if not (is_dirty and random.random() < 0.5) else None,
        "event_type": random.choice(EVENT_TYPES),
        "item_id": random.choice(ITEM_IDS),
        "timestamp": datetime.utcnow().isoformat() if not (is_dirty and random.random() < 0.5) else "invalid_date"
    }
    return event

def simulate(rate_per_second=5):
    print(f"Starting simulation. Sending events to {API_URL} at {rate_per_second} req/s...")
    delay = 1.0 / rate_per_second
    
    while True:
        event = generate_event()
        try:
            response = requests.post(API_URL, json=event)
            if response.status_code == 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Event sent: {event['event_type']} by {event['user_id']}")
            else:
                print(f"Failed to send event. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending event: {str(e)}")
            
        time.sleep(delay)

if __name__ == "__main__":
    # Note: Update API_URL before running
    simulate(rate_per_second=2)
