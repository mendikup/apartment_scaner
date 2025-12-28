import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailNotifier:
    """Handles formatting and sending email alerts."""

    def __init__(self, sender, password, receiver):
        self.sender = sender
        self.password = password
        self.receiver = receiver

    def send_alert(self, info):
        """Formats the apartment data and sends it via SMTP."""
        subject = f"New Apt Found: {info['city']} - {info['price']} NIS"

        # Email body structure
        body = f"""
        A new apartment matching your search was found:

        City: {info['city']}
        Street: {info['street']}
        Rooms: {info['rooms']}
        Floor: {info['floor']}
        Price: {info['price']} NIS

        Direct Link: {info['link']}
        """

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            # Connect to Gmail SMTP server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender, self.password)
                server.send_message(msg)
            print(f"[+] Alert email sent for ID: {info['id']}")
        except Exception as e:
            print(f"[!] SMTP Error: {e}")