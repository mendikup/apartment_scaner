import os

class LocalStore:
    """Manages a local file to keep track of already seen advertisements."""
    def __init__(self, filename="seen_ads.txt"):
        self.filename = filename
        self.seen_ids = self._load_seen_ids()

    def _load_seen_ids(self):
        """Loads IDs from the text file into a set for fast lookup."""
        if not os.path.exists(self.filename):
            return set()
        with open(self.filename, "r") as f:
            return set(line.strip() for line in f)

    def is_new(self, ad_id):
        """Returns True if the ID has not been seen before."""
        return str(ad_id) not in self.seen_ids

    def save_id(self, ad_id):
        """Appends a new ID to the local file and the memory set."""
        self.seen_ids.add(str(ad_id))
        with open(self.filename, "a") as f:
            f.write(f"{ad_id}\n")