import requests

class Yad2Client:
    """Handles all communications with the Yad2 API."""
    def __init__(self, url):
        self.url = url
        # Headers to mimic a real browser request
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.yad2.co.il/realestate/rent"        }

    def fetch_listings(self):
        """Fetches the latest listings from the API and returns the 'markers' list."""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status() # Raise error for bad status codes (4xx, 5xx)
            data = response.json()
            # Navigating the JSON structure based on the map API response
            return data.get('data', {}).get('markers', [])
        except Exception as e:
            print(f"[!] API Error: {e}")
            return []