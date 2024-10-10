import os

def get_notifier_url():
    host = os.getenv("APP_HOST")
    sender_port = os.getenv("SENDER_PORT")
    return f"http://{host}:{sender_port}/send_email"