import os
import time
import random  # <--- New import
from dotenv import load_dotenv
from yad_2_client import Yad2Client
from storage import LocalStore
from notifier import EmailNotifier

load_dotenv()

# ================= CONFIGURATION FROM ENV =================
SEARCH_URL = os.getenv("SEARCH_URL")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Define range instead of fixed interval
MIN_INTERVAL = int(os.getenv("MIN_INTERVAL", 480))
MAX_INTERVAL = int(os.getenv("MAX_INTERVAL", 720))


# ==========================================================

class ApartmentMonitor:
    def __init__(self):
        self.client = Yad2Client(SEARCH_URL)
        self.store = LocalStore()
        self.notifier = EmailNotifier(EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECEIVER)

    def run_cycle(self):
        """Single check cycle"""
        print(f"[*] Checking for updates at {time.ctime()}...")
        listings = self.client.fetch_listings()

        for item in listings:
            ad_id = item.get('orderId')
            if ad_id and self.store.is_new(ad_id):
                address_data = item.get('address', {})
                details_data = item.get('additionalDetails', {})

                info = {
                    'id': ad_id,
                    'city': address_data.get('city', {}).get('text', 'N/A'),
                    'street': address_data.get('street', {}).get('text', 'N/A'),
                    'rooms': details_data.get('roomsCount', 'N/A'),
                    'price': item.get('price', 'N/A'),
                    'floor': item.get('house', {}).get('floor', 'N/A'),
                    'link': f"https://www.yad2.co.il/realestate/item/{item.get('token')}"}
                self.notifier.send_alert(info)
                self.store.save_id(ad_id)

    def start(self):
        """Starts the infinite loop with random sleep duration."""
        print(f"--- Yad2 Monitor Started (Range: {MIN_INTERVAL}-{MAX_INTERVAL}s) ---")
        while True:
            self.run_cycle()

            # Calculate a random wait time for the next run
            wait_time = random.randint(MIN_INTERVAL, MAX_INTERVAL)
            print(f"[*] Sleeping for {wait_time} seconds before next check...")
            time.sleep(wait_time)


if __name__ == "__main__":
    monitor = ApartmentMonitor()
    monitor.start()